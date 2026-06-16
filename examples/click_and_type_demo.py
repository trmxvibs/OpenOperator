import time

from openoperator.action.mouse import MouseActionController
from openoperator.action.keyboard import KeyboardActionController


def main() -> None:
    print("Move mouse to target area in 5 seconds...")
    time.sleep(5)

    mouse = MouseActionController()
    keyboard = KeyboardActionController()

    x = 500
    y = 500

    mouse.move_mouse(x, y)
    mouse.click()

    time.sleep(1)

    keyboard.type_text(
        "Hello from OpenOperator Click + Type Demo"
    )

    print("Demo completed")


if __name__ == "__main__":
    main()