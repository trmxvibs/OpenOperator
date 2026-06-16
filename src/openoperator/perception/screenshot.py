from io import BytesIO

from mss import mss
from PIL import Image


class ScreenshotEngine:
    """
    Captures screenshots and returns PNG bytes.
    """

    def capture_screen(self) -> bytes:
        with mss() as sct:
            monitor = sct.monitors[1]

            screenshot = sct.grab(monitor)

            image = Image.frombytes(
                "RGB",
                screenshot.size,
                screenshot.rgb,
            )

            buffer = BytesIO()

            image.save(
                buffer,
                format="PNG",
            )

            return buffer.getvalue()
