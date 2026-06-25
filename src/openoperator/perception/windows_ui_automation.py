"""
Windows UI Automation Provider.

Foundation implementation.

Future versions will integrate Microsoft's
UI Automation COM interfaces.
"""

import logging
import sys

from openoperator.perception.accessibility import AccessibilityTree
from openoperator.perception.ui_automation import UIAutomationProvider

logger = logging.getLogger(__name__)


class WindowsUIAutomationProvider(UIAutomationProvider):
    """
    Windows accessibility provider.

    Currently returns an empty accessibility tree.

    Future implementation will populate the tree
    using Windows UI Automation APIs.
    """

    def get_accessibility_tree(self) -> AccessibilityTree:
        if sys.platform != "win32":
            logger.warning(
                "Windows UI Automation is only supported on Windows."
            )
            return AccessibilityTree()

        return AccessibilityTree()