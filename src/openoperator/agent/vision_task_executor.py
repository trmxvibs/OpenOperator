"""
Vision task executor module for OpenOperator.

This module provides a high-level orchestration pipeline that combines OS-level 
window management with vision-guided targeting, keyboard input, and OCR verification.
"""

import logging
import time
from typing import Optional

from openoperator.action.keyboard import KeyboardActionController
from openoperator.action.window_controller import WindowController
from openoperator.agent.vision_actor import VisionActor
from openoperator.core.verification import VerificationEngine
from openoperator.perception.ocr import OCREngine
from openoperator.perception.screenshot import ScreenshotEngine

logger = logging.getLogger(__name__)


class VisionTaskExecutor:
    """
    High-level orchestrator that executes a complete GUI automation sequence:
    Focus Window -> Locate Target -> Click -> Type -> Verify.
    """

    def __init__(
        self,
        window_controller: Optional[WindowController] = None,
        vision_actor: Optional[VisionActor] = None,
        keyboard_controller: Optional[KeyboardActionController] = None,
        screenshot_engine: Optional[ScreenshotEngine] = None,
        ocr_engine: Optional[OCREngine] = None,
        verification_engine: Optional[VerificationEngine] = None,
    ) -> None:
        """
        Initializes the VisionTaskExecutor with all required subsystems.
        Uses dependency injection with fallbacks to default instances.
        """
        self.window = window_controller or WindowController()
        self.actor = vision_actor or VisionActor()
        self.keyboard = keyboard_controller or KeyboardActionController()
        self.screenshot = screenshot_engine or ScreenshotEngine()
        self.ocr = ocr_engine or OCREngine()
        self.verification = verification_engine or VerificationEngine()

    def execute(
        self,
        window_title: str,
        click_text: str,
        type_text: str,
        verify_text: str,
        delay_between_steps: float = 1.0
    ) -> bool:
        """
        Executes a targeted sequence of GUI actions and verifies the outcome.

        Args:
            window_title (str): The substring to search for to focus the target window.
            click_text (str): The multi-word text phrase to locate and click on screen.
            type_text (str): The string to type after clicking the target.
            verify_text (str): The text expected to be on screen to confirm success.
            delay_between_steps (float): Time to wait (in seconds) between OS actions.

        Returns:
            bool: True if the entire sequence completed and verification succeeded, False otherwise.
        """
        logger.info(f"Starting VisionTask sequence for target window: '{window_title}'")

        try:
            # 1. Focus Target Window
            logger.info(f"Step 1: Attempting to focus window '{window_title}'")
            focus_success = self.window.focus_window_by_title(window_title)
            if not focus_success:
                logger.error("Sequence aborted: Failed to focus target window.")
                return False
            
            time.sleep(delay_between_steps)

            # 2 & 3. Locate Target and Click
            logger.info(f"Step 2 & 3: Locating and clicking target text '{click_text}'")
            click_success = self.actor.click_text(click_text)
            if not click_success:
                logger.error("Sequence aborted: Failed to locate or click target text.")
                return False
                
            time.sleep(delay_between_steps)

            # 4. Type Text
            logger.info(f"Step 4: Typing text '{type_text}'")
            type_success = self.keyboard.type_text(type_text)
            if not type_success:
                logger.error("Sequence aborted: Failed to execute typing action.")
                return False
                
            time.sleep(delay_between_steps)

            # 5. Capture Screenshot
            logger.info("Step 5: Capturing screen for verification.")
            image_bytes = self.screenshot.capture_screen()
            if not image_bytes:
                logger.error("Sequence aborted: Screen capture failed.")
                return False

            # 6. OCR Extraction
            logger.info("Step 6: Extracting OCR text from screenshot.")
            screen_text = self.ocr.extract_text(image_bytes)
            if not screen_text:
                logger.error("Sequence aborted: No text extracted from screen.")
                return False

            # 7. Verification
            logger.info(f"Step 7: Verifying presence of '{verify_text}'")
            verification_result = self.verification.verify_text_present(
                expected_text=verify_text,
                screen_text=screen_text
            )

            if verification_result.success:
                logger.info("VisionTask completed successfully. Verification passed.")
                return True
            else:
                logger.warning(f"VisionTask failed verification: {verification_result.reason}")
                return False

        except Exception as e:
            logger.error(f"Unexpected error during VisionTask execution: {e}", exc_info=True)
            return False