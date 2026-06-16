from openoperator.agent.dummy import DummyAgent
from openoperator.core.orchestrator import OpenOperator
from openoperator.perception.screenshot import ScreenshotEngine


class MockController:

    def move_mouse(self, x: int, y: int) -> bool:
        return True

    def click(self, button: str = "left") -> bool:
        return True

    def type_text(self, text: str) -> bool:
        return True


def test_orchestrator_creation() -> None:

    operator = OpenOperator(
        perception=ScreenshotEngine(),
        controller=MockController(),
        brain=DummyAgent(),
    )

    assert operator is not None
