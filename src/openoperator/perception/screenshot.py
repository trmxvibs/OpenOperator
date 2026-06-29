"""
Screenshot module for OpenOperator.
Upgraded for high-performance, real-time screen capture using a persistent MSS session.
"""

import logging
from io import BytesIO

from mss import MSS
from PIL import Image

logger = logging.getLogger(__name__)


class ScreenshotEngine:
    """
    Captures screenshots and returns PNG bytes.
    Optimized for high-frequency captures during autonomous loops.
    """

    def __init__(self) -> None:
        """
        Initializes a persistent MSS session to avoid the massive overhead
        of creating a new context manager on every single frame capture.
        """
        self.sct = MSS()
        # sct.monitors[1] is typically the primary monitor
        self.monitor = self.sct.monitors[1]
        logger.debug("ScreenshotEngine initialized with a persistent MSS session.")

    def capture_screen(self) -> bytes:
        """
        Capture the primary monitor and return PNG bytes rapidly.
        """
        try:
            # Grab the raw pixels from the screen
            screenshot = self.sct.grab(self.monitor)

            # Convert raw RGB pixels to a PIL Image
            image = Image.frombytes(
                "RGB",
                screenshot.size,
                screenshot.rgb,
            )

            buffer = BytesIO()

            # compress_level=1 prioritizes speed over file size,
            # which is crucial for real-time agent perception.
            image.save(
                buffer,
                format="PNG",
                compress_level=1
            )

            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Failed to capture screen: {e}")
            return b""

    def capture(self) -> bytes:
        """
        Backward-compatible alias for legacy tests and modules.

        Returns:
            bytes: PNG image bytes.
        """
        return self.capture_screen()

    def __del__(self) -> None:
        """
        Ensure the MSS session is properly closed when the engine is destroyed.
        """
        try:
            self.sct.close()
        except Exception:
            pass