import logging

from pynput.keyboard import Controller

logger = logging.getLogger(__name__)


class KeyboardActionController:
    """
    Cross-platform keyboard controller.
    """

    def __init__(self) -> None:
        self.keyboard = Controller()

    def type_text(
        self,
        text: str,
    ) -> bool:
        try:
            self.keyboard.type(text)

            logger.info(
                "Typed text: %s",
                text,
            )

            return True

        except Exception as exc:
            logger.error(
                "Failed typing text: %s",
                exc,
            )

            return False
