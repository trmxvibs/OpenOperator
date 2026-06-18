"""
Window controller module for OpenOperator.

This module provides OS-level window management capabilities, such as focusing
specific application windows by their title.
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
                "Calls on this OS will return False."
            )

    def focus_window_by_title(self, title: str) -> bool:
        """
        Searches for a visible window containing the specified title and brings it
        to the foreground. If the window is minimized, it is restored.

        Performs a case-insensitive, partial match (e.g., "notepad" matches "Untitled - Notepad").

        Args:
            title (str): The text to search for in the window title.

        Returns:
            bool: True if a matching window was found and successfully focused, False otherwise.
        """
        if sys.platform != "win32":
            logger.error("focus_window_by_title is only supported on Windows.")
            return False

        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32
        
        # SW_RESTORE constant for ShowWindow ensures minimized windows are restored
        SW_RESTORE = 9

        found_hwnd: Optional[int] = None
        search_title = title.lower()

        # Define the callback type for EnumWindows
        WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

        def enum_windows_proc(hwnd: int, lParam: int) -> bool:
            """Callback function to inspect each top-level window."""
            nonlocal found_hwnd
            
            # Skip invisible windows (background processes, hidden toolbars)
            if user32.IsWindowVisible(hwnd):
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buff, length + 1)
                    window_text = buff.value.lower()
                    
                    if search_title in window_text:
                        found_hwnd = hwnd
                        # Return False to stop enumerating once we find a match
                        return False
                        
            # Return True to continue enumerating
            return True

        logger.debug(f"Scanning open windows for title containing: '{title}'")
        
        # Enumerate all top level windows. 
        # (EnumWindows returns 0 if the callback returns False, meaning we found our target)
        user32.EnumWindows(WNDENUMPROC(enum_windows_proc), 0)

        if found_hwnd:
            logger.debug(f"Found match. HWND: {found_hwnd}. Attempting to focus...")
            
            # Restore the window in case it is minimized
            user32.ShowWindow(found_hwnd, SW_RESTORE)
            
            # Bring the window to the foreground
            success = user32.SetForegroundWindow(found_hwnd)
            
            if success:
                logger.info(f"Successfully focused window matching '{title}'.")
                return True
            else:
                logger.warning(
                    f"Found window matching '{title}', but OS denied foreground request. "
                    "This can happen if another application holds strict focus."
                )
                return False

        logger.warning(f"No visible window found matching title: '{title}'.")
        return False