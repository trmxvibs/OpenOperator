"""
Abstract UI Automation provider.

Defines the interface for platform-specific
accessibility providers.
"""

from abc import ABC
from abc import abstractmethod

from openoperator.perception.accessibility import AccessibilityTree


class UIAutomationProvider(ABC):
    """
    Base interface for UI Automation providers.

    Platform implementations should inherit from this class.
    """

    @abstractmethod
    def get_accessibility_tree(self) -> AccessibilityTree:
        """
        Returns the current accessibility tree.

        Returns:
            AccessibilityTree
        """
        raise NotImplementedError