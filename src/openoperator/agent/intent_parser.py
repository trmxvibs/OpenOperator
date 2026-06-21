"""
Intent parser module for OpenOperator.

This module provides a deterministic, regex-based natural language parser 
that translates unstructured prompts into a structured VisionTaskPlan.
"""

import logging
import re
from typing import Optional

from openoperator.agent.action_memory_manager import ActionMemoryManager
from openoperator.agent.vision_models import VisionActionType, VisionStep, VisionTaskPlan

logger = logging.getLogger(__name__)


class VisionIntentParser:
    """
    Parses unstructured natural language prompts into structured VisionTaskPlans
    using regex patterns to extract actionable intents and parameters.
    """

    def __init__(self, memory: Optional[ActionMemoryManager] = None) -> None:
        """
        Initializes the VisionIntentParser with supported verb groupings and 
        optional session memory for context-aware parsing.
        """
        self.memory = memory
        self.focus_verbs = {"open", "switch to", "focus"}
        self.click_verbs = {"click"}
        self.type_verbs = {"type", "enter"}
        self.verify_verbs = {"verify", "check", "confirm"}
        
        # Build the combined regex pattern dynamically
        all_verbs = (
            list(self.focus_verbs) + 
            list(self.click_verbs) + 
            list(self.type_verbs) + 
            list(self.verify_verbs)
        )
        
        # Sort by length descending to ensure compound verbs ("switch to") 
        # match before their individual parts, should any overlap exist in the future.
        all_verbs.sort(key=len, reverse=True)
        
        # Escape and join verbs for the regex pattern
        escaped_verbs = [re.escape(v) for v in all_verbs]
        verbs_pattern = "|".join(escaped_verbs)
        
        # Regex captures the verb and everything after it until the next verb or end of string
        self.pattern = re.compile(
            rf'\b({verbs_pattern})\b(.*?)(?=\b(?:{verbs_pattern})\b|$)', 
            re.IGNORECASE
        )

    def parse(self, prompt: str) -> VisionTaskPlan:
        """
        Parses a natural language string into a sequence of vision steps.

        Args:
            prompt (str): The unstructured natural language instruction.

        Returns:
            VisionTaskPlan: The compiled structured execution plan.
        """
        logger.debug(f"Parsing vision intent from prompt: '{prompt}'")
        
        steps: list[VisionStep] = []
        missing_context: list[str] = []
        is_executable = True
        
        matches = list(self.pattern.finditer(prompt))
        step_id = 1
        
        # Check if the prompt already contains an explicit focus command
        has_explicit_focus = any(
            match.group(1).lower() in self.focus_verbs for match in matches
        )
        
        # Context-Aware Follow-Up Injection
        # If no explicit focus is requested, but the user wants to type or click,
        # we infer they want to perform the action on the last active window.
        if not has_explicit_focus and self.memory and self.memory.last_window:
            has_actionable_verb = any(
                match.group(1).lower() in self.click_verbs or 
                match.group(1).lower() in self.type_verbs 
                for match in matches
            )
            
            if has_actionable_verb:
                logger.debug(f"Injecting inferred context: FOCUS_WINDOW -> '{self.memory.last_window}'")
                steps.append(
                    VisionStep(
                        step_id=step_id,
                        action_type=VisionActionType.FOCUS_WINDOW,
                        target_element=self.memory.last_window,
                        confidence=1.0
                    )
                )
                step_id += 1

        for match in matches:
            verb = match.group(1).lower()
            
            # Extract the raw argument captured between verbs
            arg = match.group(2)
            
            # Remove trailing sequence connectors ("and", "then", "next") 
            # to prevent them from attaching to the target parameters.
            arg = re.sub(r'(?i)(\b(and|then|next)\b[\s,]*)+$', '', arg)
            
            # Strip remaining leading/trailing whitespace and common punctuation
            arg = arg.strip(" ,.")
            
            action_type = None
            target_element = None
            input_data = None
            confidence = 1.0  # Rule-based matches default to 100% confidence
            
            if verb in self.focus_verbs:
                action_type = VisionActionType.FOCUS_WINDOW
                target_element = arg
                if not target_element:
                    missing_context.append(f"Missing window name for '{verb}' action.")
                    is_executable = False
                    
            elif verb in self.click_verbs:
                action_type = VisionActionType.CLICK_TEXT
                # Strip noise words (e.g., "click on file" -> "file")
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
                steps.append(
                    VisionStep(
                        step_id=step_id,
                        action_type=action_type,
                        target_element=target_element,
                        input_data=input_data,
                        confidence=confidence
                    )
                )
                step_id += 1
                
        if not steps:
            is_executable = False
            missing_context.append("No valid action keywords found in the prompt.")
            logger.warning("Parser could not extract any valid steps.")
        else:
            logger.info(f"Successfully parsed {len(steps)} steps from prompt.")
            
        return VisionTaskPlan(
            original_prompt=prompt,
            steps=steps,
            is_executable=is_executable,
            missing_context=missing_context
        )