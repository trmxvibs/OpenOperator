from openoperator.action.mouse import MouseActionController


def test_mouse_controller_creation() -> None:
    controller = MouseActionController()

    assert controller is not None
