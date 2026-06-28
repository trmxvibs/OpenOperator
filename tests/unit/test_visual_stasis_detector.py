"""
Tests for VisualStasisDetector.
Verifies that the agent can correctly identify when the screen stops changing.
"""

import pytest
from openoperator.agent.visual_stasis_detector import VisualStasisDetector


def test_stasis_not_triggered_early():
    """Test that stasis is not falsely triggered before reaching max_history."""
    detector = VisualStasisDetector(max_history=3)
    detector.add_observation("Screen State A")
    detector.add_observation("Screen State A")
    
    assert detector.is_in_stasis() is False


def test_stasis_triggered():
    """Test that stasis returns True when max_history identical frames are reached."""
    detector = VisualStasisDetector(max_history=3)
    detector.add_observation("Static Screen")
    detector.add_observation("Static Screen")
    detector.add_observation("Static Screen")
    
    assert detector.is_in_stasis() is True


def test_stasis_broken_by_change():
    """Test that introducing a new screen state resets the stasis condition."""
    detector = VisualStasisDetector(max_history=3)
    detector.add_observation("Static Screen")
    detector.add_observation("Static Screen")
    detector.add_observation("New Screen State")
    
    assert detector.is_in_stasis() is False


def test_clear_history():
    """Test that clearing the history resets the stasis detector entirely."""
    detector = VisualStasisDetector(max_history=3)
    detector.add_observation("Static")
    detector.add_observation("Static")
    detector.add_observation("Static")
    
    assert detector.is_in_stasis() is True
    
    detector.clear()
    assert detector.is_in_stasis() is False


def test_ignore_empty_observations():
    """Test that empty screen text is ignored to prevent false stasis on blank screens."""
    detector = VisualStasisDetector(max_history=3)
    detector.add_observation("Screen A")
    detector.add_observation("")
    detector.add_observation(None)
    
    assert len(detector.history) == 1