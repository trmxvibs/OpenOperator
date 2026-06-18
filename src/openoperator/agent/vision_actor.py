import logging
from typing import Optional

from openoperator.action.mouse import MouseActionController
from openoperator.perception.locator import TextLocatorEngine
from openoperator.perception.screenshot import ScreenshotEngine

logger = logging.getLogger(__name__)


class VisionActor:

    def __init__(
        self,
        screenshot_engine: Optional[ScreenshotEngine] = None,
        locator_engine: Optional[TextLocatorEngine] = None,
        mouse_controller: Optional[MouseActionController] = None,
    ) -> None:

        self.screenshot = screenshot_engine or ScreenshotEngine()
        self.locator = locator_engine or TextLocatorEngine()
        self.mouse = mouse_controller or MouseActionController()

    def click_text(
        self,
        target_text: str,
    ) -> bool:

        logger.info(
            f"Searching screen for text: '{target_text}'"
        )

        image_bytes = self.screenshot.capture_screen()

        if not image_bytes:
            logger.warning("Screen capture failed.")
            return False

        targets = self.locator.find_text_targets(
            image_bytes=image_bytes,
            search_text=target_text,
        )

        if not targets:
            logger.warning(
                f"Target not found: {target_text}"
            )
            return False

        best_target = targets[0]

        logger.info(
            f"Matched text='{best_target.text}' "
            f"confidence={best_target.confidence}"
        )

        logger.info(
            f"Target found at "
            f"({best_target.center_x}, {best_target.center_y})"
        )

        self.mouse.move_mouse(
            best_target.center_x,
            best_target.center_y,
        )

        self.mouse.click("left")

        return True