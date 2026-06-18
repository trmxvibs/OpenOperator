import logging
import re

from openoperator.agent.vision_models import (
    VisionActionType,
    VisionStep,
    VisionTaskPlan,
)

logger = logging.getLogger(__name__)


class VisionIntentParser:

    def __init__(self) -> None:

        self.focus_verbs = {"open", "switch to", "focus"}
        self.click_verbs = {"click"}
        self.type_verbs = {"type", "enter"}
        self.verify_verbs = {"verify", "check", "confirm"}

        all_verbs = (
            list(self.focus_verbs)
            + list(self.click_verbs)
            + list(self.type_verbs)
            + list(self.verify_verbs)
        )

        all_verbs.sort(key=len, reverse=True)

        escaped_verbs = [
            re.escape(v)
            for v in all_verbs
        ]

        verbs_pattern = "|".join(escaped_verbs)

        self.pattern = re.compile(
            rf"\b({verbs_pattern})\b(.*?)(?=\b(?:{verbs_pattern})\b|$)",
            re.IGNORECASE,
        )

    def parse(
        self,
        prompt: str,
    ) -> VisionTaskPlan:

        steps: list[VisionStep] = []
        missing_context: list[str] = []

        is_executable = True
        step_id = 1

        matches = self.pattern.finditer(prompt)

        for match in matches:

            verb = match.group(1).lower()

            arg = match.group(2)

            arg = re.sub(
                r"(?i)(\b(and|then|next)\b[\s,]*)+$",
                "",
                arg,
            )

            arg = arg.strip(" ,.")

            action_type = None
            target_element = None
            input_data = None

            if verb in self.focus_verbs:

                action_type = VisionActionType.FOCUS_WINDOW
                target_element = arg

                if not target_element:
                    is_executable = False
                    missing_context.append(
                        f"Missing window name for '{verb}' action."
                    )

            elif verb in self.click_verbs:

                action_type = VisionActionType.CLICK_TEXT

                if arg.lower().startswith("on "):
                    arg = arg[3:].strip()

                target_element = arg

                if not target_element:
                    is_executable = False
                    missing_context.append(
                        f"Missing target text for '{verb}' action."
                    )

            elif verb in self.type_verbs:

                action_type = VisionActionType.TYPE_TEXT
                input_data = arg

                if not input_data:
                    is_executable = False
                    missing_context.append(
                        f"Missing input text for '{verb}' action."
                    )

            elif verb in self.verify_verbs:

                action_type = VisionActionType.VERIFY_STATE
                input_data = arg

                if not input_data:
                    is_executable = False
                    missing_context.append(
                        f"Missing expected text for '{verb}' action."
                    )

            if action_type:

                steps.append(
                    VisionStep(
                        step_id=step_id,
                        action_type=action_type,
                        target_element=target_element,
                        input_data=input_data,
                        confidence=1.0,
                    )
                )

                step_id += 1

        if not steps:

            is_executable = False

            missing_context.append(
                "No valid action keywords found in the prompt."
            )

        return VisionTaskPlan(
            original_prompt=prompt,
            steps=steps,
            is_executable=is_executable,
            missing_context=missing_context,
        )