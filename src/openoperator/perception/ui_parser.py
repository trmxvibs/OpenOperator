"""
Dynamic UI Parser for OpenOperator.

Converts raw screen images into structured JSON UI element trees.
Extracts spatial coordinates (bounding boxes), text, and confidence scores
to give the agent a structured understanding of the GUI.
"""

import io
import logging
from typing import Any, Dict, List

import pytesseract
from PIL import Image

logger = logging.getLogger(__name__)


class DynamicUIParser:
    """
    Parses raw images into structured UI element trees using deep OCR data.
    """

    def parse_ui_elements(self, image_bytes: bytes, confidence_threshold: int = 40) -> List[Dict[str, Any]]:
        """
        Extracts text with spatial bounding boxes to form a UI component list.

        Args:
            image_bytes (bytes): The raw screenshot bytes.
            confidence_threshold (int): Minimum OCR confidence score to consider valid.

        Returns:
            List[Dict[str, Any]]: A list of structured UI elements containing text and spatial bounds.
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            # Using output_type=DICT to get spatial bounding box data instead of just strings
            ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            ui_elements = []
            n_boxes = len(ocr_data['text'])
            
            for i in range(n_boxes):
                text = ocr_data['text'][i].strip()
                conf = int(ocr_data['conf'][i])
                
                # Filter out empty text blocks, whitespace, or low confidence artifacts
                if text and conf >= confidence_threshold:
                    element = {
                        "text": text,
                        "bounds": {
                            "left": ocr_data['left'][i],
                            "top": ocr_data['top'][i],
                            "width": ocr_data['width'][i],
                            "height": ocr_data['height'][i]
                        },
                        "confidence": conf
                    }
                    ui_elements.append(element)
                    
            logger.info(f"Dynamically parsed {len(ui_elements)} UI elements from the screen.")
            return ui_elements
            
        except Exception as e:
            logger.error(f"Failed to parse UI elements: {e}", exc_info=True)
            return []