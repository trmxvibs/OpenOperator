from dataclasses import dataclass
from typing import Optional
import logging

from openoperator.action.window_controller import WindowController
from openoperator.perception.ocr import OCREngine
from openoperator.perception.screenshot import ScreenshotEngine

logger = logging.getLogger(__name__)


@dataclass
class ScreenState:
    active_window: Optional[str]
    visible_text: str
    raw_image: bytes


class ScreenStateAnalyzer:

    def __init__(
        self,
        screenshot_engine=None,
        ocr_engine=None,
        window_controller=None,
    ):
        self.screenshot_engine = screenshot_engine or ScreenshotEngine()
        self.ocr_engine = ocr_engine or OCREngine()
        self.window_controller = window_controller or WindowController()

    def analyze(self):

        raw_image = self.screenshot_engine.capture_screen()

        if not raw_image:
            return None

        try:
            active_window = (
                self.window_controller.get_active_window_title()
            )
        except Exception:
            active_window = None

        try:
            visible_text = self.ocr_engine.extract_text(raw_image)

            if visible_text is None:
                visible_text = ""

        except Exception:
            visible_text = ""

        return ScreenState(
            active_window=active_window,
            visible_text=visible_text,
            raw_image=raw_image,
        )