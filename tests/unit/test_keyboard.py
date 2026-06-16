from openoperator.action.keyboard import KeyboardActionController


def test_keyboard_controller_creation() -> None:
    controller = KeyboardActionController()

    assert controller is not None
