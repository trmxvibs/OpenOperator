"""
Screen analyzer module for OpenOperator.

Combines screenshot capture and OCR extraction to provide a structured
analysis of the current screen state.
"""

import logging
from typing import Optional

from pydantic import BaseModel

from openoperator.perception.ocr import OCREngine
from openoperator.perception.screenshot import ScreenshotEngine

logger = logging.getLogger(__name__)


class ScreenAnalysis(BaseModel):
    """
    Structured data model representing the parsed text from a screen state.
    """
    text: str
    word_count: int
    line_count: int


class ScreenAnalyzer:
    """
    High-level analyzer that captures the screen and extracts text using OCR.
    """

    def __init__(
        self,
        screenshot_engine: Optional[ScreenshotEngine] = None,
        ocr_engine: Optional[OCREngine] = None,
    ) -> None:
        """
        Initializes the ScreenAnalyzer.

        Args:
            screenshot_engine: Injected ScreenshotEngine. Defaults to a new instance.
            ocr_engine: Injected OCREngine. Defaults to a new instance.
        """
        self.screenshot_engine = screenshot_engine or ScreenshotEngine()
        self.ocr_engine = ocr_engine or OCREngine()

    def analyze_screen(self) -> ScreenAnalysis:
        """
        Captures the current screen state, performs OCR, and computes text statistics.

        Returns:
            ScreenAnalysis: A structured object containing the raw text,
                            word count, and line count.
        """
        logger.debug("Starting screen analysis...")
        
        try:
            image_bytes = self.screenshot_engine.capture_screen()
            
            if not image_bytes:
                logger.warning("Screen capture returned empty bytes.")
                return ScreenAnalysis(text="", word_count=0, line_count=0)

            text = self.ocr_engine.extract_text(image_bytes)
            
            if not text:
                logger.debug("No text detected on the screen.")
                return ScreenAnalysis(text="", word_count=0, line_count=0)

            word_count = len(text.split())
            line_count = len(text.splitlines())

            logger.debug(f"Screen analysis complete: {word_count} words, {line_count} lines found.")
            
            return ScreenAnalysis(
                text=text,
                word_count=word_count,
                line_count=line_count,
            )

        except Exception as e:
            logger.error(f"Failed to analyze screen: {e}", exc_info=True)
            return ScreenAnalysis(text="", word_count=0, line_count=0)