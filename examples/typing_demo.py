import time

from openoperator.action.keyboard import KeyboardActionController


def main() -> None:
    keyboard = KeyboardActionController()

    print("Open Notepad...")
    print("Typing starts in 5 seconds...")

    time.sleep(5)

    keyboard.type_text(
        "Hello from OpenOperator"
    )

    print("Done")


if __name__ == "__main__":
    main()