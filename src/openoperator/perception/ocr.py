"""
OCR engine for OpenOperator using Tesseract.

This module provides optical character recognition capabilities
to extract raw text from screen captures or UI elements.
"""

import io
import logging

import pytesseract
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)


class OCREngine:
    """
    Production-ready OCR engine utilizing pytesseract and Pillow.
    """

    def __init__(self, tesseract_cmd: str | None = None) -> None:
        """
        Initializes the OCR Engine.

        Args:
            tesseract_cmd (str | None): Optional path to the tesseract executable.
                                        If provided, configures pytesseract to use it.
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            logger.debug(f"Configured tesseract_cmd path: {tesseract_cmd}")

    def extract_text(self, image_bytes: bytes) -> str:
        """
        Extracts text from the provided image bytes using OCR.

        Args:
            image_bytes (bytes): The raw image data (e.g., PNG, JPEG bytes).

        Returns:
            str: The extracted text, stripped of leading/trailing whitespace.
                 Returns an empty string if OCR fails or no text is found.
        """
        if not image_bytes:
            logger.warning("Empty image bytes provided to OCR engine.")
            return ""

        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            if image.mode not in ("RGB", "L", "RGBA"):
                image = image.convert("RGB")
                
            text = pytesseract.image_to_string(image)
            return text.strip()
            
        except UnidentifiedImageError:
            logger.error("Failed to extract text: Provided bytes are not a valid image format.")
            return ""
        except pytesseract.TesseractNotFoundError:
            logger.error(
                "Tesseract is not installed or not in your PATH. "
                "Please install Tesseract-OCR to use the OCREngine."
            )
            return ""
        except Exception as e:
            logger.error(f"Unexpected error during OCR extraction: {e}", exc_info=True)
            return ""