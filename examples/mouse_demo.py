import time

from openoperator.action.mouse import MouseActionController


def main() -> None:
    mouse = MouseActionController()

    print("Moving mouse in 3 seconds...")

    time.sleep(3)

    mouse.move_mouse(500, 500)

    print("Done")


if __name__ == "__main__":
    main()