"""
Task runner module for OpenOperator Vision Planning.

This module provides the execution orchestration layer. It accepts a compiled
VisionTaskPlan and routes each discrete step to the appropriate OS or Vision subsystem.
Upgraded with Dynamic Execution capabilities to handle UI delays, loading times, and automatic retries.
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

    def execute_plan(
        self, 
        plan: VisionTaskPlan, 
        delay_between_steps: float = 1.0, 
        max_retries: int = 3, 
        dynamic_delay: float = 1.5
    ) -> bool:
        """
        Iterates through the compiled VisionTaskPlan and executes each step dynamically.
        If a step fails (e.g., due to UI load times), it will retry before aborting.

        Args:
            plan (VisionTaskPlan): The sequence of steps to execute.
            delay_between_steps (float): Time to wait (in seconds) between successful OS actions.
            max_retries (int): Maximum number of attempts per step.
            dynamic_delay (float): Time to wait (in seconds) between retries.

        Returns:
            bool: True if all steps executed successfully, False if any step ultimately failed.
        """
        logger.info(f"Starting dynamic execution for prompt: '{plan.original_prompt}'")

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

            # Dynamic Retry Loop for handling asynchronous OS delays
            for attempt in range(max_retries):
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
                            success = False
                        else:
                            logger.debug("Extracting OCR text...")
                            screen_text = self.ocr.extract_text(image_bytes)

                            if not screen_text:
                                logger.error("OCR extraction failed during verification.")
                                success = False
                            else:
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

                    # If successful, break out of the retry loop
                    if success:
                        break
                    
                    # If failed but we still have retries left, wait and try again
                    if attempt < max_retries - 1:
                        logger.warning(f"Step {step.step_id} failed. Retrying in {dynamic_delay}s... (Attempt {attempt + 2}/{max_retries})")
                        time.sleep(dynamic_delay)

                except Exception as e:
                    logger.error(f"Unexpected error during Step {step.step_id}: {e}", exc_info=True)
                    if attempt < max_retries - 1:
                        time.sleep(dynamic_delay)
                    else:
                        return False

            # Halt entire execution if all retries failed
            if not success:
                logger.error(f"Execution aborted. Failed at Step {step.step_id} ({step.action_type.value}) after {max_retries} attempts.")
                return False

            # Allow OS a tiny moment to catch up before instantly firing the next step
            time.sleep(delay_between_steps)

        logger.info("VisionTaskPlan execution completed successfully.")
        return True