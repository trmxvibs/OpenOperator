"""
Window controller module for OpenOperator.

This module provides OS-level window management capabilities, such as focusing
specific application windows by their title, detecting the currently active
window, and checking window states.
"""

import logging
import sys
from typing import Optional

logger = logging.getLogger(__name__)


class WindowController:
    """
    Controller responsible for interacting with desktop windows via the OS API.

    Currently implemented using the Windows API (user32.dll) via ctypes to avoid
    heavy external dependencies. Cross-platform compatibility stubs are included.
    """

    def __init__(self) -> None:
        """Initializes the WindowController and checks platform compatibility."""
        if sys.platform != "win32":
            logger.warning(
                "WindowController is currently only implemented for Windows. "
                "Calls on this OS will return False or None."
            )

    def get_active_window_title(self) -> Optional[str]:
        """
        Returns the title of the currently active foreground window.

        Returns:
            Optional[str]:
                Active window title if available.
                None if detection fails.
        """

        if sys.platform != "win32":
            logger.warning("get_active_window_title is only supported on Windows.")
            return None

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

    def is_window_active(self, title: str) -> bool:
        """
        Checks if the currently active window matches the target title.
        Provides window state awareness to prevent redundant focus calls.
        """
        active_title = self.get_active_window_title()
        if not active_title:
            return False
        
        return title.lower() in active_title.lower()

    def focus_window_by_title(self, title: str) -> bool:
        """
        Searches for a visible window containing the specified title and brings it
        to the foreground. If the window is minimized, it is restored.
        Skips the focus request if the window is already active.

        Performs a case-insensitive, partial match.
        """

        if sys.platform != "win32":
            logger.error("focus_window_by_title is only supported on Windows.")
            return False

        # State Awareness: Check if it's already focused
        if self.is_window_active(title):
            logger.debug(f"Window '{title}' is already active. Skipping focus call.")
            return True

        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32
        SW_RESTORE = 9

        found_hwnd: Optional[int] = None
        search_title = title.lower()

        WNDENUMPROC = ctypes.WINFUNCTYPE(
            wintypes.BOOL,
            wintypes.HWND,
            wintypes.LPARAM,
        )

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

            # Restore if minimized
            user32.ShowWindow(found_hwnd, SW_RESTORE)
            
            # Bring to front
            success = user32.SetForegroundWindow(found_hwnd)

            if success:
                logger.info(f"Successfully focused window matching '{title}'.")
                return True

            logger.warning(f"Found window matching '{title}', but OS denied foreground request.")
            return False

        logger.warning(f"No visible window found matching title: '{title}'.")
        return False