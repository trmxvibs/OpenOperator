from mss import mss


class ScreenshotEngine:
    def capture(self) -> bytes:
        with mss() as sct:
            monitor = sct.monitors[1]
            image = sct.grab(monitor)

            return image.rgb
