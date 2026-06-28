"""
Windows UI Automation Provider.

Populates the accessibility tree using Windows UI Automation APIs
via the 'uiautomation' library.
"""

import logging
import sys

from openoperator.perception.accessibility import AccessibilityTree, AccessibilityElement
from openoperator.perception.ui_automation import UIAutomationProvider

logger = logging.getLogger(__name__)

try:
    import uiautomation as auto
    _UIA_AVAILABLE = True
except ImportError:
    _UIA_AVAILABLE = False


class WindowsUIAutomationProvider(UIAutomationProvider):
    """
    Windows accessibility provider.
    
    Dynamically reads the currently active window's UI elements
    and maps them to the OpenOperator AccessibilityTree.
    """

    def get_accessibility_tree(self) -> AccessibilityTree:
        tree = AccessibilityTree()

        if sys.platform != "win32":
            logger.warning("Windows UI Automation is only supported on Windows.")
            return tree

        if not _UIA_AVAILABLE:
            logger.error(
                "The 'uiautomation' package is missing. "
                "Please run 'pip install uiautomation' to enable this feature."
            )
            return tree

        try:
            # We grab the foreground (active) window to keep the tree small and relevant.
            # Scanning the entire desktop takes too long and adds noise.
            root_control = auto.GetForegroundControl()

            if not root_control:
                return tree

            self._walk_control_tree(root_control, tree)
            
        except Exception as e:
            logger.error(f"Failed to fetch Windows UI Automation tree: {e}")

        return tree

    def _walk_control_tree(self, control, tree: AccessibilityTree) -> None:
        """
        Recursively walks the UI control tree and populates our generic AccessibilityTree.
        """
        try:
            # Extract basic properties
            name = control.Name
            control_type = control.ControlTypeName

            rect = control.BoundingRectangle
            left, top = rect.left, rect.top
            width = rect.right - rect.left
            height = rect.bottom - rect.top

            # Only add elements that have actual screen presence
            if width > 0 and height > 0:
                element = AccessibilityElement(
                    name=name or "",
                    control_type=control_type or "",
                    left=left,
                    top=top,
                    width=width,
                    height=height,
                    enabled=control.IsEnabled,
                    interactable=True  # Can be expanded based on focusability
                )
                tree.add(element)

            # Traverse children recursively
            for child in control.GetChildren():
                self._walk_control_tree(child, tree)

        except Exception:
            # Some dynamic UI controls might disappear during traversal, 
            # or restrict access. We safely ignore them and continue.
            pass