"""
Cross-Platform Window Controller module for OpenOperator.
Provides OS-level window management (focusing, state detection) for Windows, macOS, and Linux.
"""

import logging
import sys
from abc import ABC, abstractmethod
from typing import Optional

logger = logging.getLogger(__name__)


class BaseWindowController(ABC):
    """Abstract base class ensuring a standard interface for OS-specific window controllers."""

    @abstractmethod
    def focus_window_by_title(self, title: str) -> bool:
        """Searches for a window by title and brings it to the foreground."""
        pass

    @abstractmethod
    def get_active_window_title(self) -> Optional[str]:
        """Returns the title of the currently active/focused window."""
        pass

    def is_window_active(self, title: str) -> bool:
        """
        State-awareness: Checks if the currently active window matches the target title.
        This logic is OS-agnostic and uses the underlying get_active_window_title method.
        """
        active_title = self.get_active_window_title()
        if not active_title:
            return False
        return title.lower() in active_title.lower()


class WindowsWindowController(BaseWindowController):
    """Windows OS native implementation using ctypes and user32.dll."""
    
    def focus_window_by_title(self, title: str) -> bool:
        if self.is_window_active(title):
            logger.debug(f"Window '{title}' is already active. Skipping focus call.")
            return True

        # Imports are kept inside the method to prevent import errors on Mac/Linux
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32
        SW_RESTORE = 9

        found_hwnd: Optional[int] = None
        search_title = title.lower()

        WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

        def enum_windows_proc(hwnd: int, lParam: int) -> bool:
            nonlocal found_hwnd
            if user32.IsWindowVisible(hwnd):
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buff, length + 1)
                    window_text = buff.value.lower()
                    if search_title in window_text:
                        found_hwnd = hwnd
                        return False
            return True

        logger.debug(f"Scanning open windows for title containing: '{title}'")
        user32.EnumWindows(WNDENUMPROC(enum_windows_proc), 0)

        if found_hwnd:
            logger.debug(f"Found match. HWND: {found_hwnd}. Attempting to focus...")
            user32.ShowWindow(found_hwnd, SW_RESTORE)
            success = user32.SetForegroundWindow(found_hwnd)
            
            if success:
                logger.info(f"Successfully focused window matching '{title}'.")
                return True
                
            logger.warning(f"Found window matching '{title}', but OS denied foreground request.")
            return False

        logger.warning(f"No visible window found matching title: '{title}'.")
        return False

    def get_active_window_title(self) -> Optional[str]:
        try:
            import ctypes
            user32 = ctypes.windll.user32
            
            hwnd = user32.GetForegroundWindow()
            if not hwnd:
                return None
                
            length = user32.GetWindowTextLengthW(hwnd)
            if length <= 0:
                return None
                
            buffer = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buffer, length + 1)
            title = buffer.value.strip()
            
            if not title:
                return None
                
            return title
            
        except Exception as e:
            logger.error(f"Failed to get active window title: {e}")
            return None


class MacOSWindowController(BaseWindowController):
    """Apple macOS implementation (Stub - to be implemented with AppleScript/Quartz)."""
    
    def focus_window_by_title(self, title: str) -> bool:
        logger.warning("MacOS focus_window_by_title is a stub. Community PRs welcome!")
        return False

    def get_active_window_title(self) -> Optional[str]:
        return None


class LinuxWindowController(BaseWindowController):
    """Linux implementation (Stub - to be implemented with wmctrl/xdotool)."""
    
    def focus_window_by_title(self, title: str) -> bool:
        logger.warning("Linux focus_window_by_title is a stub. Community PRs welcome!")
        return False

    def get_active_window_title(self) -> Optional[str]:
        return None


class WindowController:
    """
    Factory class that dynamically instantiates and returns the correct
    OS-specific window controller based on the host operating system.
    """
    
    def __new__(cls):
        if sys.platform == "win32":
            return WindowsWindowController()
        elif sys.platform == "darwin":
            return MacOSWindowController()
        elif sys.platform.startswith("linux"):
            return LinuxWindowController()
        else:
            logger.warning(f"Unsupported OS: {sys.platform}. Falling back to Linux stub.")
            return LinuxWindowController()