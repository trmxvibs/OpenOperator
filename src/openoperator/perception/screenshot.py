from io import BytesIO
import time

from mss import mss
from PIL import Image

from openoperator.config import RETRY_DELAY, MAX_RETRIES


class ScreenshotEngine:
    """
    Captures screenshots and returns PNG bytes.
    """

    def capture_screen(self) -> bytes:
        """
        Capture the primary monitor and return PNG bytes.
        Reintenta MAX_RETRIES veces si falla.
        """
        for intento in range(MAX_RETRIES):
            try:
                with mss() as sct:
                    monitor = sct.monitors[1]
                    screenshot = sct.grab(monitor)
                    image = Image.frombytes(
                        "RGB",
                        screenshot.size,
                        screenshot.rgb,
                    )
                    buffer = BytesIO()
                    image.save(buffer, format="PNG")
                    return buffer.getvalue()
            except Exception as e:
                print(f"Captura falló (intento {intento + 1}/{MAX_RETRIES}): {e}")
                if intento < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
        return b""

    def capture(self) -> bytes:
        """
        Backward-compatible alias for legacy tests and modules.

        Returns:
            bytes: PNG image bytes.
        """
        return self.capture_screen()
