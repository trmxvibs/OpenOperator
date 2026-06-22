from io import BytesIO

from mss import MSS
from PIL import Image


class ScreenshotEngine:
    """
    Captures screenshots and returns PNG bytes.
    """

    def capture_screen(self) -> bytes:
        """
        Capture the primary monitor and return PNG bytes.
        """
        with MSS() as sct:
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

    def capture(self) -> bytes:
        """
        Backward-compatible alias for legacy tests and modules.

        Returns:
            bytes: PNG image bytes.
        """
        return self.capture_screen()