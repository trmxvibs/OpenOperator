import logging

from pynput.mouse import Button
from pynput.mouse import Controller

logger = logging.getLogger(__name__)


class MouseActionController:
    """
    Cross-platform mouse controller.
    """

    def __init__(self) -> None:
        self.mouse = Controller()

    def move_mouse(self, x: int, y: int) -> bool:
        try:
            self.mouse.position = (x, y)

            logger.info(
                "Mouse moved to (%s, %s)",
                x,
                y,
            )

            return True

        except Exception as exc:
            logger.error(
                "Failed moving mouse: %s",
                exc,
            )

            return False

    def click(
        self,
        button: str = "left",
    ) -> bool:
        try:

            button_map = {
                "left": Button.left,
                "right": Button.right,
                "middle": Button.middle,
            }

            target_button = button_map.get(
                button.lower(),
                Button.left,
            )

            self.mouse.click(
                target_button,
                1,
            )

            logger.info(
                "Mouse clicked (%s)",
                button,
            )

            return True

        except Exception as exc:
            logger.error(
                "Failed clicking mouse: %s",
                exc,
            )

            return False
