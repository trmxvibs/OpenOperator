"""
Goal Completion Detector module for OpenOperator.

This module provides the GoalCompletionDetector class, which evaluates whether
a natural language goal has been achieved based on the current screen text.
"""

import logging
import re

logger = logging.getLogger(__name__)


class GoalCompletionDetector:
    """
    Evaluates screen text against a natural language goal to determine completion.
    """

    def __init__(self) -> None:
        """Initializes the GoalCompletionDetector."""
        pass

    def _extract_target(self, goal: str) -> str:
        """
        Extracts the primary target text to verify from the goal string.
        
        Args:
            goal (str): The natural language goal.
            
        Returns:
            str: The extracted target phrase or word.
        """
        # Extract text within quotes if present
        quote_match = re.search(r"['\"](.*?)['\"]", goal)
        if quote_match:
            return quote_match.group(1)
        
        # Fallback keyword extraction: remove common verbs and stop words
        words = goal.split()
        stopwords = {"verify", "check", "confirm", "is", "open", "that", "the"}
        target_words = [w for w in words if w.lower() not in stopwords]
        
        return " ".join(target_words)

    def is_goal_completed(self, goal: str, screen_text: str) -> bool:
        """
        Evaluates if the goal is satisfied by the current screen text.

        Args:
            goal (str): The natural language goal.
            screen_text (str): The OCR extracted text from the screen.

        Returns:
            bool: True if the goal is completed, False otherwise.
        """
        if not goal or not screen_text:
            return False
            
        target = self._extract_target(goal)
        if not target:
            return False
            
        pattern = r"\b" + re.escape(target) + r"\b"
        return (
            re.search(
                pattern,
                screen_text,
                flags=re.IGNORECASE,
            )
            is not None
        )