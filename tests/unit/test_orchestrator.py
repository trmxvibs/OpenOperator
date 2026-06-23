from openoperator.core.orchestrator import OpenOperator
from openoperator.perception.screenshot import ScreenshotEngine


class MockController:

    def move_mouse(self, x: int, y: int) -> bool:
        return True

    def click(self, button: str = "left") -> bool:
        return True

    def type_text(self, text: str) -> bool:
        return True


class MockAgent:

    def decide_next_action(self, goal, image_data):
        return None


def test_orchestrator_creation() -> None:

    operator = OpenOperator(
        perception=ScreenshotEngine(),
        controller=MockController(),
        brain=MockAgent(),
    )

    assert operator is not None