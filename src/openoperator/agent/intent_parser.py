"""
Intent parser module for OpenOperator.

This module provides a dual-engine natural language parser:
1. LLMIntentParser: A modern, pluggable LLM-based intent parser for complex instructions.
2. VisionIntentParser: A deterministic, regex-based fallback parser for fast, offline execution.
"""

import json
import logging
import os
import re
import urllib.request
import urllib.error
from typing import Optional, List, Dict, Any

from openoperator.agent.action_memory_manager import ActionMemoryManager
from openoperator.agent.vision_models import VisionActionType, VisionStep, VisionTaskPlan

logger = logging.getLogger(__name__)

LLM_SYSTEM_PROMPT = """You are an AI desktop automation agent. Your task is to translate user natural language commands into a strict JSON array of execution steps.
Users may provide instructions in English, Hindi, or Hinglish (e.g., 'notepad khol do aur hello type karo').

Allowed Action Types:
- FOCUS_WINDOW: Brings an application to the foreground. Requires 'target_element' (the window name).
- CLICK_TEXT: Clicks on specific text on the screen. Requires 'target_element' (the text to click).
- TYPE_TEXT: Types strings using the keyboard. Requires 'input_data' (the text to type).
- VERIFY_STATE: Checks if text exists on the screen. Requires 'input_data' (the expected text).

Context Rule: If the user asks to type or click without explicitly stating which window to open first, do NOT invent a FOCUS_WINDOW step.

Output ONLY a valid JSON array. No markdown formatting, no explanations.
Format example: [{"action_type": "FOCUS_WINDOW", "target_element": "Notepad"}, {"action_type": "TYPE_TEXT", "input_data": "hello world"}]
"""

class VisionIntentParser:
    """
    Parses unstructured natural language prompts into structured VisionTaskPlans
    using regex patterns to extract actionable intents and parameters.
    """

    def __init__(self, memory: Optional[ActionMemoryManager] = None) -> None:
        self.memory = memory
        self.focus_verbs = {"open", "switch to", "focus"}
        self.click_verbs = {"click"}
        self.type_verbs = {"type", "enter"}
        self.verify_verbs = {"verify", "check", "confirm"}
        
        all_verbs = (
            list(self.focus_verbs) + 
            list(self.click_verbs) + 
            list(self.type_verbs) + 
            list(self.verify_verbs)
        )
        all_verbs.sort(key=len, reverse=True)
        escaped_verbs = [re.escape(v) for v in all_verbs]
        verbs_pattern = "|".join(escaped_verbs)
        
        self.pattern = re.compile(
            rf'\b({verbs_pattern})\b(.*?)(?=\b(?:{verbs_pattern})\b|$)', 
            re.IGNORECASE
        )

    def parse(self, prompt: str) -> VisionTaskPlan:
        logger.debug(f"Parsing vision intent (Regex Fallback) from prompt: '{prompt}'")
        steps: list[VisionStep] = []
        missing_context: list[str] = []
        is_executable = True
        
        matches = list(self.pattern.finditer(prompt))
        step_id = 1
        
        has_explicit_focus = any(match.group(1).lower() in self.focus_verbs for match in matches)
        if not has_explicit_focus and self.memory and self.memory.last_window:
            has_actionable_verb = any(
                match.group(1).lower() in self.click_verbs or match.group(1).lower() in self.type_verbs 
                for match in matches
            )
            if has_actionable_verb:
                logger.debug(f"Injecting inferred context: FOCUS_WINDOW -> '{self.memory.last_window}'")
                steps.append(
                    VisionStep(
                        step_id=step_id, action_type=VisionActionType.FOCUS_WINDOW, target_element=self.memory.last_window, confidence=1.0
                    )
                )
                step_id += 1

        for match in matches:
            verb = match.group(1).lower()
            arg = match.group(2)
            arg = re.sub(r'(?i)(\b(and|then|next)\b[\s,]*)+$', '', arg).strip(" ,.")
            
            action_type, target_element, input_data = None, None, None
            
            if verb in self.focus_verbs:
                action_type = VisionActionType.FOCUS_WINDOW
                target_element = arg
                if not target_element:
                    missing_context.append(f"Missing window name for '{verb}' action.")
                    is_executable = False
            elif verb in self.click_verbs:
                action_type = VisionActionType.CLICK_TEXT
                if arg.lower().startswith("on "):
                    arg = arg[3:].strip()
                target_element = arg
                if not target_element:
                    missing_context.append(f"Missing target text for '{verb}' action.")
                    is_executable = False
            elif verb in self.type_verbs:
                action_type = VisionActionType.TYPE_TEXT
                input_data = arg
                if not input_data:
                    missing_context.append(f"Missing input text for '{verb}' action.")
                    is_executable = False
            elif verb in self.verify_verbs:
                action_type = VisionActionType.VERIFY_STATE
                input_data = arg
                if not input_data:
                    missing_context.append(f"Missing expected text for '{verb}' action.")
                    is_executable = False
            
            if action_type:
                steps.append(VisionStep(step_id=step_id, action_type=action_type, target_element=target_element, input_data=input_data, confidence=1.0))
                step_id += 1
                
        if not steps:
            is_executable = False
            missing_context.append("No valid action keywords found in the prompt.")
            logger.warning("Regex Parser could not extract any valid steps.")
        else:
            logger.info(f"Successfully parsed {len(steps)} steps using Regex fallback.")
            
        return VisionTaskPlan(original_prompt=prompt, steps=steps, is_executable=is_executable, missing_context=missing_context)


class LLMIntentParser(VisionIntentParser):
    """
    Advanced parser utilizing an LLM (Local Ollama or Remote API) to understand 
    complex, multi-step, and multi-lingual commands.
    Falls back gracefully to the Regex parser if the LLM API is unreachable.
    """

    def __init__(self, memory: Optional[ActionMemoryManager] = None, endpoint: str = None, model: str = None, api_key: str = None) -> None:
        super().__init__(memory)
        # Default config targets local Ollama to ensure offline privacy out-of-the-box
        self.endpoint = endpoint or os.getenv("LLM_ENDPOINT", "http://localhost:11434/v1/chat/completions")
        self.model = model or os.getenv("LLM_MODEL", "llama3")
        self.api_key = api_key or os.getenv("LLM_API_KEY", "")

    def parse(self, prompt: str) -> VisionTaskPlan:
        logger.debug(f"Attempting LLM parsing for prompt: '{prompt}'")
        try:
            steps_data = self._call_llm(prompt)
            
            steps = []
            step_id = 1
            
            has_explicit_focus = any(s.get("action_type") == "FOCUS_WINDOW" for s in steps_data)
            if not has_explicit_focus and self.memory and self.memory.last_window:
                has_actionable = any(s.get("action_type") in ["CLICK_TEXT", "TYPE_TEXT"] for s in steps_data)
                if has_actionable:
                    logger.debug(f"LLM inferred context injection: FOCUS_WINDOW -> '{self.memory.last_window}'")
                    steps.append(
                        VisionStep(step_id=step_id, action_type=VisionActionType.FOCUS_WINDOW, target_element=self.memory.last_window, confidence=1.0)
                    )
                    step_id += 1

            for data in steps_data:
                action_str = data.get("action_type", "")
                try:
                    action_type = VisionActionType[action_str]
                except KeyError:
                    logger.warning(f"LLM returned invalid action_type: {action_str}")
                    continue
                    
                steps.append(
                    VisionStep(
                        step_id=step_id,
                        action_type=action_type,
                        target_element=data.get("target_element"),
                        input_data=data.get("input_data"),
                        confidence=0.95  # Slightly lower confidence to indicate AI prediction
                    )
                )
                step_id += 1

            if not steps:
                raise ValueError("LLM returned empty or invalid step sequence.")

            logger.info(f"Successfully parsed {len(steps)} steps using LLM Engine.")
            return VisionTaskPlan(original_prompt=prompt, steps=steps, is_executable=True, missing_context=[])

        except Exception as e:
            logger.warning(f"LLM parsing failed ({e}). Falling back to Regex NLP parser.")
            return super().parse(prompt)

    def _call_llm(self, prompt: str) -> List[Dict[str, Any]]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": LLM_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.0
        }

        req = urllib.request.Request(
            self.endpoint, 
            data=json.dumps(payload).encode('utf-8'), 
            headers=headers, 
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=8.0) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        content = result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
            
        return json.loads(content.strip())