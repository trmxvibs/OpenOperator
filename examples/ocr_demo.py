from openoperator.perception.screenshot import ScreenshotEngine
from openoperator.perception.ocr import OCREngine


def main() -> None:
    screenshot_engine = ScreenshotEngine()
    ocr_engine = OCREngine()

    print("Capturing screen...")

    image_bytes = screenshot_engine.capture_screen()

    print("Running OCR...")

    text = ocr_engine.extract_text(image_bytes)

    print("\n===== DETECTED TEXT =====\n")
    print(text)
    print("\n=========================\n")


if __name__ == "__main__":
    main()