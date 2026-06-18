import logging

from openoperator.perception.locator import TextLocatorEngine
from openoperator.perception.screenshot import ScreenshotEngine


def main() -> None:

    logging.basicConfig(level=logging.INFO)

    screenshot = ScreenshotEngine()
    locator = TextLocatorEngine()

    search_phrase = "chat"

    print(f"Searching for: {search_phrase}")

    image_bytes = screenshot.capture_screen()

    targets = locator.find_text_targets(
        image_bytes=image_bytes,
        search_text=search_phrase,
    )

    print()

    if not targets:
        print("NOT FOUND")
        return

    print("FOUND TARGETS")
    print()

    for target in targets:

        print("TEXT:", target.text)
        print("CENTER:", target.center_x, target.center_y)
        print("CONFIDENCE:", target.confidence)
        print()


if __name__ == "__main__":
    main()