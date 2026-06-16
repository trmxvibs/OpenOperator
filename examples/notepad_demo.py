import time

from openoperator.action.keyboard import KeyboardActionController


def main() -> None:
    print("=================================")
    print("Open Notepad manually")
    print("Click inside Notepad")
    print("Typing starts in 5 seconds")
    print("=================================")

    time.sleep(5)

    keyboard = KeyboardActionController()

    keyboard.type_text(
        "Hello from OpenOperator!\n"
        "This text was typed automatically.\n"
        "Open-source AI computer operator.\n"
    )

    print("Demo completed")


if __name__ == "__main__":
    main()