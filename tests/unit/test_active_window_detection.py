"""
Tests for Active Window Detection across platforms.
Verifies the WindowController Factory and OS-specific implementations.
"""

import pytest
from unittest.mock import patch, MagicMock
from openoperator.action.window_controller import (
    WindowController,
    WindowsWindowController,
    LinuxWindowController,
    MacOSWindowController
)

def test_factory_returns_windows_controller_on_win32():
    """Test that the Factory returns the Windows implementation on Windows."""
    with patch("sys.platform", "win32"):
        controller = WindowController()
        assert isinstance(controller, WindowsWindowController)

def test_factory_returns_linux_controller_on_linux():
    """Test that the Factory returns the Linux implementation on Linux."""
    with patch("sys.platform", "linux"):
        controller = WindowController()
        assert isinstance(controller, LinuxWindowController)

def test_factory_returns_mac_controller_on_darwin():
    """Test that the Factory returns the MacOS implementation on Darwin."""
    with patch("sys.platform", "darwin"):
        controller = WindowController()
        assert isinstance(controller, MacOSWindowController)

def test_linux_get_active_window_title_is_none():
    """Test that the Linux stub safely returns None."""
    controller = LinuxWindowController()
    assert controller.get_active_window_title() is None

def test_mac_get_active_window_title_is_none():
    """Test that the Mac stub safely returns None."""
    controller = MacOSWindowController()
    assert controller.get_active_window_title() is None

def test_windows_get_active_window_title_handles_no_window():
    """Test Windows controller gracefully handles when no window is foreground."""
    controller = WindowsWindowController()
    with patch("ctypes.windll.user32.GetForegroundWindow", return_value=0):
        assert controller.get_active_window_title() is None

def test_windows_get_active_window_title_success():
    """Test Windows controller correctly retrieves window title."""
    controller = WindowsWindowController()
    
    with patch("ctypes.windll.user32.GetForegroundWindow", return_value=12345), \
         patch("ctypes.windll.user32.GetWindowTextLengthW", return_value=11), \
         patch("ctypes.windll.user32.GetWindowTextW") as mock_get_text:
        
        # Mocking ctypes buffer injection
        def side_effect(hwnd, buffer, length):
            buffer.value = "Test Window"
            return 11
        
        mock_get_text.side_effect = side_effect
        
        assert controller.get_active_window_title() == "Test Window"