"""
Demonstration of the upgraded TextLocatorEngine utilizing text normalization
and N-gram sliding windows to bypass OCR tokenization artifacts for multi-word targets.
"""

import logging

from openoperator.perception.locator import TextLocatorEngine
from openoperator.perception.screenshot import ScreenshotEngine


def main() -> None:
    # Configure standardized architecture logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    logger.info("Initializing Screenshot and Locator engines...")
    screenshot = ScreenshotEngine()
    locator = TextLocatorEngine()

    search_phrase = "New chat"
    
    logger.info("Capturing screen state...")
    image_bytes = screenshot.capture_screen()
    
    if not image_bytes:
        logger.error("Failed to capture screen.")
        return

    logger.info(f"Searching for target phrase: '{search_phrase}' (fuzzy matching enabled)")
    
    # Executes the pipeline using standard built-in difflib logic
    targets = locator.find_text_targets(
        image_bytes=image_bytes, 
        search_text=search_phrase, 
        exact_match=False
    )

    if not targets:
        logger.warning(f"Phrase '{search_phrase}' could not be located on the screen.")
        return

    print("\n" + "=" * 50)
    print(f"DETECTED TARGETS FOR: '{search_phrase}'")
    print("=" * 50)
    
    for idx, target in enumerate(targets, start=1):
        # Dump nested Pydantic models neatly to stdout
        print(f"TARGET #{idx}:")
        print(target.model_dump_json(indent=4))
        print("-" * 50)
        
    logger.info("Phrase Click Demo complete.")


if __name__ == "__main__":
    main()