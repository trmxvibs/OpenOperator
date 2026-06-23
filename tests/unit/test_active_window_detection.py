from unittest.mock import patch

from openoperator.action.window_controller import WindowController


def test_get_active_window_title_exists():
    controller = WindowController()

    assert hasattr(controller, "get_active_window_title")


def test_returns_none_when_not_windows():
    controller = WindowController()

    with patch("sys.platform", "linux"):
        result = controller.get_active_window_title()

    assert result is None


def test_returns_string_or_none():
    controller = WindowController()

    result = controller.get_active_window_title()

    assert result is None or isinstance(result, str)


def test_backward_compatibility():
    controller = WindowController()

    assert hasattr(controller, "focus_window_by_title")