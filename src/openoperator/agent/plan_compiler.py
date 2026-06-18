"""
Vision Plan Compiler for OpenOperator.

Validates and compiles VisionTaskPlan objects into executable plans.
"""

import logging

from openoperator.agent.vision_models import (
    VisionActionType,
    VisionTaskPlan,
)

logger = logging.getLogger(__name__)


class VisionPlanCompiler:
    """
    Validates and compiles parsed VisionTaskPlans.
    """

    def compile(
        self,
        plan: VisionTaskPlan,
    ) -> VisionTaskPlan:

        if not plan.steps:
            plan.is_executable = False

            if (
                "No valid action keywords found in the prompt."
                not in plan.missing_context
            ):
                plan.missing_context.append(
                    "No executable steps available."
                )

            return plan

        seen_focus = False
        seen_click = False

        for step in plan.steps:

            if step.action_type == VisionActionType.FOCUS_WINDOW:

                seen_focus = True

                if not step.target_element:
                    plan.is_executable = False

                    plan.missing_context.append(
                        "FOCUS_WINDOW requires target_element."
                    )

            elif step.action_type == VisionActionType.CLICK_TEXT:

                seen_click = True

                if not step.target_element:
                    plan.is_executable = False

                    plan.missing_context.append(
                        "CLICK_TEXT requires target_element."
                    )

            elif step.action_type == VisionActionType.TYPE_TEXT:

                if not step.input_data:
                    plan.is_executable = False

                    plan.missing_context.append(
                        "TYPE_TEXT requires input_data."
                    )

                if not seen_focus and not seen_click:
                    plan.is_executable = False

                    plan.missing_context.append(
                        "TYPE_TEXT requires a prior FOCUS_WINDOW or CLICK_TEXT."
                    )

            elif step.action_type == VisionActionType.VERIFY_STATE:

                if not step.input_data:
                    plan.is_executable = False

                    plan.missing_context.append(
                        "VERIFY_STATE requires input_data."
                    )

        if plan.is_executable:
            logger.info(
                "VisionTaskPlan compiled successfully."
            )
        else:
            logger.warning(
                "VisionTaskPlan compilation failed."
            )

        return plan