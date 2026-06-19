"""
Action memory manager module for OpenOperator.

This module provides session memory capabilities to track the agent's recent 
actions, including the last focused window, clicked target, and typed text.
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ActionMemoryManager:
    """
    Manages the session state and action history for the OpenOperator agent.
    """

    def __init__(self) -> None:
        """Initializes an empty action memory state."""
        self.last_window: Optional[str] = None
        self.last_click: Optional[str] = None
        self.last_typed: Optional[str] = None
        self.action_history: List[str] = []

    def remember_window(self, window_name: str) -> None:
        """
        Records the last successfully focused window.
        
        Args:
            window_name (str): The title or identifier of the window.
        """
        self.last_window = window_name
        self.action_history.append(f"Focused window: {window_name}")
        logger.debug(f"Memory updated: Focused window '{window_name}'")

    def remember_click(self, target: str) -> None:
        """
        Records the last successfully clicked text target.
        
        Args:
            target (str): The text that was clicked.
        """
        self.last_click = target
        self.action_history.append(f"Clicked text: {target}")
        logger.debug(f"Memory updated: Clicked '{target}'")

    def remember_type(self, text: str) -> None:
        """
        Records the last successfully typed text string.
        
        Args:
            text (str): The text that was typed.
        """
        self.last_typed = text
        self.action_history.append(f"Typed text: {text}")
        logger.debug(f"Memory updated: Typed '{text}'")

    def get_memory(self) -> Dict[str, Any]:
        """
        Retrieves the current state of the session memory.
        
        Returns:
            Dict[str, Any]: A dictionary containing current memory fields and history.
        """
        return {
            "last_window": self.last_window,
            "last_click": self.last_click,
            "last_typed": self.last_typed,
            "action_history": self.action_history.copy(),
        }

    def clear(self) -> None:
        """Clears all stored memory and action history."""
        self.last_window = None
        self.last_click = None
        self.last_typed = None
        self.action_history.clear()
        logger.debug("Action memory cleared.")