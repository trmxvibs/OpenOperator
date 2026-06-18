import io
import logging

import pytesseract
from PIL import Image
from pytesseract import Output

from openoperator.core.models import BoundingBox, UITarget

logger = logging.getLogger(__name__)


class TextLocatorEngine:

    def find_text_targets(
        self,
        image_bytes: bytes,
        search_text: str,
        exact_match: bool = False,
    ) -> list[UITarget]:

        image = Image.open(io.BytesIO(image_bytes))

        data = pytesseract.image_to_data(
            image,
            output_type=Output.DICT,
        )

        results: list[UITarget] = []

        for i in range(len(data["text"])):

            detected_text = data["text"][i].strip()

            if not detected_text:
                continue

            matched = False

            if exact_match:
                matched = detected_text == search_text
            else:
                matched = search_text.lower() in detected_text.lower()

            if not matched:
                continue

            left = data["left"][i]
            top = data["top"][i]
            width = data["width"][i]
            height = data["height"][i]

            center_x = left + (width // 2)
            center_y = top + (height // 2)

            try:
                confidence = float(data["conf"][i])
            except Exception:
                confidence = 0.0

            results.append(
                UITarget(
                    text=detected_text,
                    box=BoundingBox(
                        x=left,
                        y=top,
                        width=width,
                        height=height,
                    ),
                    center_x=center_x,
                    center_y=center_y,
                    confidence=confidence,
                )
            )

        results.sort(
            key=lambda item: item.confidence,
            reverse=True,
        )

        return results