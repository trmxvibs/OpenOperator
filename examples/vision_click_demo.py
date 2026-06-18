import logging
import time

from openoperator.action.mouse import MouseActionController
from openoperator.agent.vision_actor import VisionActor
from openoperator.perception.locator import TextLocatorEngine
from openoperator.perception.screenshot import ScreenshotEngine


def main() -> None:

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger(__name__)

    screenshot = ScreenshotEngine()
    locator = TextLocatorEngine()
    mouse = MouseActionController()

    actor = VisionActor(
        screenshot_engine=screenshot,
        locator_engine=locator,
        mouse_controller=mouse,
    )

    target_text = "Notebooks"

    logger.info(
        f"Demo starts in 5 seconds. "
        f"Make sure '{target_text}' is visible."
    )

    time.sleep(5)

    success = actor.click_text(target_text)

    print()

    print("SUCCESS =", success)

    print()


if __name__ == "__main__":
    main()