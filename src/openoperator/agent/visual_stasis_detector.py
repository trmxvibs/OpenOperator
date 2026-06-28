"""
Visual Stasis Detector for OpenOperator.

Detects if the autonomous agent is stuck in a loop by comparing recent 
screen observations. If the screen does not change over a set number of 
iterations, the agent is considered to be in 'stasis'.
"""

import logging

logger = logging.getLogger(__name__)


class VisualStasisDetector:
    """
    Tracks recent screen states to detect execution loops or dead UI interactions.
    """

    def __init__(self, max_history: int = 3):
        """
        Args:
            max_history (int): The number of consecutive identical observations 
                               required to trigger a stasis state.
        """
        self.max_history = max_history
        self.history: list[str] = []

    def add_observation(self, screen_text: str) -> None:
        """
        Adds a new screen text observation to the history.
        """
        if not screen_text:
            return

        if len(self.history) >= self.max_history:
            self.history.pop(0)
            
        self.history.append(screen_text.strip())
        logger.debug(f"Added observation. Current history size: {len(self.history)}")

    def is_in_stasis(self) -> bool:
        """
        Evaluates if the agent is stuck based on the observation history.
        
        Returns:
            bool: True if the last `max_history` observations are completely identical.
        """
        if len(self.history) < self.max_history:
            return False

        # Compare all stored observations against the first one in the queue
        first_obs = self.history[0]
        stuck = all(obs == first_obs for obs in self.history)
        
        if stuck:
            logger.warning("Visual Stasis Detected! The screen has not changed.")
            
        return stuck

    def clear(self) -> None:
        """
        Clears the observation history. Useful when a task is completed or reset.
        """
        self.history.clear()
        logger.debug("Stasis history cleared.")