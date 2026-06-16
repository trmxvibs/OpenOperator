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


def main() -> None:
    print("OpenOperator Demo Started")

    operator = OpenOperator(
        perception=ScreenshotEngine(),
        controller=MockController(),
        brain=DummyAgent(),
    )

    result = operator.execute_task(
        "Run basic demo",
        max_steps=1,
    )

    print(f"Result: {result}")


if __name__ == "__main__":
    main()