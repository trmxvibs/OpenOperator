"""
Task runner module for OpenOperator Vision Planning.

This module provides the execution orchestration layer. It accepts a compiled
VisionTaskPlan and routes each discrete step to the appropriate OS or Vision subsystem.
Includes Action Memory integration to maintain state context across steps.
"""

import logging
import time
from typing import Optional

from openoperator.action.keyboard import KeyboardActionController
from openoperator.action.window_controller import WindowController
from openoperator.agent.action_memory_manager import ActionMemoryManager
from openoperator.agent.vision_actor import VisionActor
from openoperator.agent.vision_models import VisionActionType, VisionTaskPlan
from openoperator.core.verification import VerificationEngine
from openoperator.perception.ocr import OCREngine
from openoperator.perception.screenshot import ScreenshotEngine

logger = logging.getLogger(__name__)


class TaskRunner:
    """
    Executes a compiled VisionTaskPlan by routing actions to specific hardware,
    OS, and perception controllers, while maintaining an active session memory.
    """

    def __init__(
        self,
        window_controller: Optional[WindowController] = None,
        vision_actor: Optional[VisionActor] = None,
        keyboard_controller: Optional[KeyboardActionController] = None,
        screenshot_engine: Optional[ScreenshotEngine] = None,
        ocr_engine: Optional[OCREngine] = None,
        verification_engine: Optional[VerificationEngine] = None,
        action_memory_manager: Optional[ActionMemoryManager] = None,
    ) -> None:
        """
        Initializes the TaskRunner with required subsystems using dependency injection.
        Fallbacks to default instances if none are provided.
        """
        self.window = window_controller or WindowController()
        self.actor = vision_actor or VisionActor()
        self.keyboard = keyboard_controller or KeyboardActionController()
        self.screenshot = screenshot_engine or ScreenshotEngine()
        self.ocr = ocr_engine or OCREngine()
        self.verification = verification_engine or VerificationEngine()
        self.memory = action_memory_manager or ActionMemoryManager()

    def execute_plan(self, plan: VisionTaskPlan, delay_between_steps: float = 1.0) -> bool:
        """
        Iterates through the compiled VisionTaskPlan and executes each step.

        Args:
            plan (VisionTaskPlan): The sequence of steps to execute.
            delay_between_steps (float): Time to wait (in seconds) between OS actions.

        Returns:
            bool: True if all steps executed successfully, False if any step failed or 
                  if the plan is marked as non-executable.
        """
        logger.info(f"Starting execution for prompt: '{plan.original_prompt}'")

        if not plan.is_executable:
            logger.error("Cannot execute plan. Plan is marked as non-executable.")
            if plan.missing_context:
                logger.error(f"Missing context: {', '.join(plan.missing_context)}")
            return False

        if not plan.steps:
            logger.warning("Execution aborted: Plan contains 0 steps.")
            return False

        for step in plan.steps:
            logger.info(f"Executing Step {step.step_id}: {step.action_type.value}")
            success = False

            try:
                if step.action_type == VisionActionType.FOCUS_WINDOW:
                    if not step.target_element:
                        logger.error("FOCUS_WINDOW requires 'target_element'.")
                        return False
                    success = self.window.focus_window_by_title(step.target_element)
                    if success and self.memory is not None:
                        self.memory.remember_window(step.target_element)

                elif step.action_type == VisionActionType.CLICK_TEXT:
                    if not step.target_element:
                        logger.error("CLICK_TEXT requires 'target_element'.")
                        return False
                    success = self.actor.click_text(step.target_element)
                    if success and self.memory is not None:
                        self.memory.remember_click(step.target_element)

                elif step.action_type == VisionActionType.TYPE_TEXT:
                    if not step.input_data:
                        logger.error("TYPE_TEXT requires 'input_data'.")
                        return False
                    success = self.keyboard.type_text(step.input_data)
                    if success and self.memory is not None:
                        self.memory.remember_type(step.input_data)

                elif step.action_type == VisionActionType.VERIFY_STATE:
                    if not step.input_data:
                        logger.error("VERIFY_STATE requires 'input_data'.")
                        return False
                        
                    logger.debug("Capturing screen for verification...")
                    image_bytes = self.screenshot.capture_screen()
                    if not image_bytes:
                        logger.error("Screen capture failed during verification.")
                        return False

                    logger.debug("Extracting OCR text...")
                    screen_text = self.ocr.extract_text(image_bytes)
                    if not screen_text:
                        logger.error("OCR extraction failed during verification.")
                        return False

                    logger.debug(f"Verifying presence of '{step.input_data}'")
                    result = self.verification.verify_text_present(
                        expected_text=step.input_data, 
                        screen_text=screen_text
                    )
                    success = result.success
                    if not success:
                        logger.warning(f"Verification failed: {result.reason}")

                else:
                    logger.error(f"Unsupported action type: {step.action_type}")
                    return False

                # Halt entire execution if a single step fails
                if not success:
                    logger.error(f"Execution aborted. Failed at Step {step.step_id} ({step.action_type.value}).")
                    return False

                # Allow OS to catch up before next step
                time.sleep(delay_between_steps)

            except Exception as e:
                logger.error(f"Unexpected error during Step {step.step_id}: {e}", exc_info=True)
                return False

        logger.info("VisionTaskPlan execution completed successfully.")
        return True