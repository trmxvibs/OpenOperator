"""
Tests for Window State Awareness in the WindowController.
Verifies that the controller can correctly identify if a window is already active
and skip redundant focus calls.
"""

import pytest
from unittest.mock import patch, MagicMock
from openoperator.action.window_controller import WindowController


@pytest.fixture
def window_controller():
    """Fixture to provide a WindowController initialized for win32 platform."""
    with patch("sys.platform", "win32"):
        return WindowController()


def test_is_window_active_matches(window_controller):
    """Test that it correctly identifies when the target window is active (case-insensitive)."""
    with patch.object(window_controller, "get_active_window_title", return_value="Untitled - Notepad"):
        assert window_controller.is_window_active("Notepad") is True
        assert window_controller.is_window_active("untitled") is True
        assert window_controller.is_window_active("UNTITLED - NOTEPAD") is True


def test_is_window_active_no_match(window_controller):
    """Test that it returns False when the target window is not the active one."""
    with patch.object(window_controller, "get_active_window_title", return_value="Google Chrome"):
        assert window_controller.is_window_active("Notepad") is False


def test_is_window_active_no_active_window(window_controller):
    """Test that it handles cases where no active window title is returned (e.g., desktop focused)."""
    with patch.object(window_controller, "get_active_window_title", return_value=None):
        assert window_controller.is_window_active("Notepad") is False


def test_focus_skips_if_already_active(window_controller):
    """Test that focus_window_by_title skips OS-level API calls if the window is already active."""
    with patch.object(window_controller, "is_window_active", return_value=True):
        # Mock ctypes EnumWindows to ensure it NEVER gets called if the window is already active
        with patch("ctypes.windll.user32.EnumWindows") as mock_enum_windows:
            result = window_controller.focus_window_by_title("Notepad")
            
            assert result is True
            mock_enum_windows.assert_not_called()