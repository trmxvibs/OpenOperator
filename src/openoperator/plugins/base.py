"""
Base Plugin Interface for OpenOperator.
All custom community plugins must inherit from this class.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class OpenOperatorPlugin(ABC):
    """
    Abstract base class defining the standard structure for all OpenOperator plugins.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique name of the plugin."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Return the version of the plugin."""
        pass

    @abstractmethod
    def initialize(self, context: Dict[str, Any]) -> None:
        """
        Called when the plugin is loaded by the PluginManager.
        Use this to set up API keys, initial state, or paths.
        """
        pass

    @abstractmethod
    def execute(self, command: str, **kwargs) -> Any:
        """
        Execute a plugin-specific command.
        
        Args:
            command (str): The specific action the plugin should perform.
            **kwargs: Dynamic arguments required for the command.
            
        Returns:
            Any: The result of the plugin execution.
        """
        pass