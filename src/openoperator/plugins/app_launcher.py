"""
App Launcher Plugin for OpenOperator.
Allows the agent to launch executable applications (like Notepad, Calculator) 
if they are not already open.
"""

import logging
import subprocess
from typing import Any, Dict

from openoperator.plugins.base import OpenOperatorPlugin

logger = logging.getLogger(__name__)


class AppLauncherPlugin(OpenOperatorPlugin):
    """
    Plugin to execute system-level application launches.
    """

    @property
    def name(self) -> str:
        return "AppLauncher"

    @property
    def version(self) -> str:
        return "1.0.0"

    def initialize(self, context: Dict[str, Any]) -> None:
        """Initialize any required state. No special context needed for basic launcher."""
        logger.debug("AppLauncherPlugin initialized.")

    def execute(self, command: str, **kwargs) -> Any:
        """
        Executes the launch command.
        
        Args:
            command (str): The specific plugin action (e.g., 'launch').
            kwargs: Must contain 'app_name' (e.g., 'notepad').
            
        Returns:
            bool: True if launch was initiated successfully, False otherwise.
        """
        if command.lower() != "launch":
            logger.warning(f"AppLauncherPlugin does not support command: '{command}'")
            return False

        app_name = kwargs.get("app_name")
        if not app_name:
            logger.error("AppLauncherPlugin requires 'app_name' keyword argument.")
            return False

        try:
            logger.info(f"Attempting to launch application: '{app_name}'")
            # Uses subprocess.Popen to launch in background without blocking the agent
            subprocess.Popen(app_name, shell=True)
            logger.info(f"Successfully initiated launch sequence for '{app_name}'")
            return True
        except Exception as e:
            logger.error(f"Failed to launch '{app_name}': {e}", exc_info=True)
            return False