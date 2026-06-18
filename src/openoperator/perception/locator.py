"""
Text locator module for OpenOperator.

Provides spatial OCR mapping to detect screen coordinates of UI elements,
supporting multi-word phrases.
"""

import io
import logging
from typing import Any

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

        # ---------- Single Word Search ----------

        if len(search_text.split()) == 1:

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

        # ---------- Multi Word Search ----------

        else:

            search_words = search_text.lower().split()

            for i in range(len(data["text"]) - len(search_words) + 1):

                candidate_words = []

                valid = True

                for j in range(len(search_words)):

                    word = data["text"][i + j].strip()

                    if not word:
                        valid = False
                        break

                    candidate_words.append(word)

                if not valid:
                    continue

                candidate_phrase = " ".join(candidate_words)

                if candidate_phrase.lower() != search_text.lower():
                    continue

                left = min(
                    data["left"][i + j]
                    for j in range(len(search_words))
                )

                top = min(
                    data["top"][i + j]
                    for j in range(len(search_words))
                )

                right = max(
                    data["left"][i + j] + data["width"][i + j]
                    for j in range(len(search_words))
                )

                bottom = max(
                    data["top"][i + j] + data["height"][i + j]
                    for j in range(len(search_words))
                )

                width = right - left
                height = bottom - top

                center_x = left + (width // 2)
                center_y = top + (height // 2)

                confidence_values = []

                for j in range(len(search_words)):
                    try:
                        confidence_values.append(
                            float(data["conf"][i + j])
                        )
                    except Exception:
                        pass

                confidence = (
                    sum(confidence_values) / len(confidence_values)
                    if confidence_values
                    else 0.0
                )

                results.append(
                    UITarget(
                        text=candidate_phrase,
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