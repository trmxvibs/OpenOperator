"""
Plugin Manager for OpenOperator.
Handles registration, loading, and execution of external plugins.
"""

import logging
from typing import Any, Dict, Type

from openoperator.plugins.base import OpenOperatorPlugin

logger = logging.getLogger(__name__)


class PluginManager:
    """
    Manages the lifecycle and execution of OpenOperator plugins.
    """

    def __init__(self) -> None:
        self._plugins: Dict[str, OpenOperatorPlugin] = {}

    def register_plugin(self, plugin_class: Type[OpenOperatorPlugin], context: Dict[str, Any] = None) -> bool:
        """
        Instantiates and registers a plugin into the manager.
        """
        if context is None:
            context = {}
            
        try:
            plugin_instance = plugin_class()
            plugin_instance.initialize(context)
            
            plugin_name = plugin_instance.name.lower()
            self._plugins[plugin_name] = plugin_instance
            
            logger.info(f"Successfully registered plugin: '{plugin_instance.name}' (v{plugin_instance.version})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register plugin '{plugin_class.__name__}': {e}", exc_info=True)
            return False

    def execute_plugin_command(self, plugin_name: str, command: str, **kwargs) -> Any:
        """
        Routes a command to a specific registered plugin.
        """
        plugin_name_lower = plugin_name.lower()
        
        if plugin_name_lower not in self._plugins:
            logger.warning(f"Cannot execute command. Plugin '{plugin_name}' is not registered.")
            return None
            
        try:
            logger.debug(f"Routing command '{command}' to plugin '{plugin_name}'")
            return self._plugins[plugin_name_lower].execute(command, **kwargs)
        except Exception as e:
            logger.error(f"Error executing command '{command}' in plugin '{plugin_name}': {e}", exc_info=True)
            return None
            
    def list_plugins(self) -> list[str]:
        """Returns a list of all currently registered plugin names."""
        return list(self._plugins.keys())