import logging
import time
from typing import Optional

from openoperator.config import MAX_RETRIES, RETRY_DELAY
from openoperator.action.mouse import MouseActionController
from openoperator.perception.locator import TextLocatorEngine
from openoperator.perception.screenshot import ScreenshotEngine

logger = logging.getLogger(__name__)


class VisionActor:

    def __init__(
        self,
        screenshot_engine: Optional[ScreenshotEngine] = None,
        locator_engine: Optional[TextLocatorEngine] = None,
        mouse_controller: Optional[MouseActionController] = None,
    ) -> None:

        self.screenshot = screenshot_engine or ScreenshotEngine()
        self.locator = locator_engine or TextLocatorEngine()
        self.mouse = mouse_controller or MouseActionController()

    def click_text(
        self,
        target_text: str,
    ) -> bool:

        for intento in range(MAX_RETRIES):
            logger.info(
                f"Buscando texto: '{target_text}' "
                f"(intento {intento + 1}/{MAX_RETRIES})"
            )

            image_bytes = self.screenshot.capture_screen()

            if not image_bytes:
                logger.warning("Captura de pantalla falló.")
                if intento < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                continue

            targets = self.locator.find_text_targets(
                image_bytes=image_bytes,
                search_text=target_text,
            )

            if not targets:
                logger.warning(f"Objetivo no encontrado: {target_text}")
                if intento < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                continue

            best_target = targets[0]

            logger.info(
                f"Encontrado: '{best_target.text}' "
                f"confianza={best_target.confidence}"
            )
            logger.info(
                f"Coordenadas: "
                f"({best_target.center_x}, {best_target.center_y})"
            )

            self.mouse.move_mouse(
                best_target.center_x,
                best_target.center_y,
            )
            self.mouse.click("left")
            return True

        logger.error(
            f"No se encontró '{target_text}' "
            f"después de {MAX_RETRIES} intentos"
        )
        return False
    