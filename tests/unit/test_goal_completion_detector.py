# D:\OpenOperator\tests\unit\test_goal_completion_detector.py

"""
Unit tests for the Goal Completion Detector.

Following Test-Driven Development (TDD), these tests define the expected 
behavior of the upcoming GoalCompletionDetector class. The tests will fail 
until the implementation is completed in Issue #37.
"""

import pytest

# Expected future import
from openoperator.core.goal_completion_detector import GoalCompletionDetector


@pytest.fixture
def detector() -> GoalCompletionDetector:
    """Provides a fresh GoalCompletionDetector instance."""
    return GoalCompletionDetector()


def test_goal_text_appears_on_screen(detector: GoalCompletionDetector) -> None:
    """Test that a goal is marked complete if its primary text is found on screen."""
    goal = "verify notepad is open"
    # Assuming the implementation will extract "notepad" as the core target
    screen_text = "File Edit Format View Help Notepad"
    
    # This test asserts basic substring/keyword presence
    assert detector.is_goal_completed(goal, screen_text) is True


def test_goal_text_absent(detector: GoalCompletionDetector) -> None:
    """Test that a goal is NOT marked complete if the text is missing."""
    goal = "verify calculator is open"
    screen_text = "File Edit Format View Help Notepad"
    
    assert detector.is_goal_completed(goal, screen_text) is False


def test_case_insensitive_matching(detector: GoalCompletionDetector) -> None:
    """Test that goal detection ignores case differences."""
    goal = "verify NOTEPAD is open"
    screen_text = "File Edit Format View Help notepad"
    
    assert detector.is_goal_completed(goal, screen_text) is True


def test_empty_goal(detector: GoalCompletionDetector) -> None:
    """Test that an empty goal string safely returns False."""
    assert detector.is_goal_completed("", "Some screen text") is False


def test_empty_screen_text(detector: GoalCompletionDetector) -> None:
    """Test that empty screen text safely returns False."""
    assert detector.is_goal_completed("verify notepad", "") is False


def test_partial_match_handling(detector: GoalCompletionDetector) -> None:
    """
    Test that the detector correctly identifies full words and doesn't 
    trigger false positives on partial overlapping strings.
    """
    goal = "verify app"
    # "apple" contains "app", but shouldn't trigger a completion for "app" as a standalone word
    screen_text = "We have an apple here."
    
    assert detector.is_goal_completed(goal, screen_text) is False


def test_multiple_words_goal_handling(detector: GoalCompletionDetector) -> None:
    """Test that the detector handles multi-word targets accurately."""
    goal = "verify 'Hello World'"
    screen_text = "The user typed Hello World successfully."
    
    assert detector.is_goal_completed(goal, screen_text) is True


def test_multiple_words_goal_missing_one_word(detector: GoalCompletionDetector) -> None:
    """Test that multi-word goals require all components (or the exact phrase)."""
    goal = "verify 'Hello World'"
    screen_text = "The user typed Hello successfully."
    
    assert detector.is_goal_completed(goal, screen_text) is False