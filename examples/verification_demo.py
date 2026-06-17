# examples/verification_demo.py

"""
Demonstration of the VerificationEngine validating screen state.
"""

import logging

from openoperator.core.verification import VerificationEngine
from openoperator.perception.ocr import OCREngine
from openoperator.perception.screenshot import ScreenshotEngine


def main() -> None:
    # Configure basic logging for the demo
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    logger.info("Initializing engines...")
    screenshot_engine = ScreenshotEngine()
    ocr_engine = OCREngine()
    verification_engine = VerificationEngine()

    logger.info("Capturing screen...")
    image_bytes = screenshot_engine.capture_screen()

    if not image_bytes:
        logger.error("Failed to capture screen. Exiting demo.")
        return

    logger.info("Extracting text via OCR...")
    screen_text = ocr_engine.extract_text(image_bytes)
    
    if not screen_text:
        logger.warning("No text extracted from the screen.")

    expected_text = "OpenOperator"
    logger.info(f"Running verification for expected text: '{expected_text}'")
    
    result = verification_engine.verify_text_present(
        expected_text=expected_text,
        screen_text=screen_text
    )

    print("\n" + "=" * 50)
    print("VERIFICATION RESULT JSON:")
    print("=" * 50)
    print(result.model_dump_json(indent=4))
    print("=" * 50 + "\n")

    logger.info("Verification demo complete.")


if __name__ == "__main__":
    main()