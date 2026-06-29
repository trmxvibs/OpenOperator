"""
Tests for the Vision Retry Strategy in the TextLocatorEngine.
Verifies that the engine correctly retries OCR scanning when targets are not found immediately.
"""

import pytest
from unittest.mock import MagicMock, patch
from openoperator.perception.locator import TextLocatorEngine, UITarget
from openoperator.core.models import BoundingBox

@pytest.fixture
def locator():
    return TextLocatorEngine()

def test_find_text_targets_with_retry_success_first_try(locator):
    """Test that it returns immediately if the target is found on the first attempt."""
    mock_image_provider = MagicMock(return_value=b"fake_image_bytes")
    mock_target = UITarget(text="Submit", box=BoundingBox(x=0, y=0, width=10, height=10), center_x=5, center_y=5, confidence=95.0)
    
    with patch.object(locator, "find_text_targets", return_value=[mock_target]) as mock_find:
        targets = locator.find_text_targets_with_retry(
            image_provider=mock_image_provider,
            search_text="Submit",
            max_attempts=3,
            retry_delay=0.1
        )
        
        assert len(targets) == 1
        assert targets[0].text == "Submit"
        assert mock_find.call_count == 1
        assert mock_image_provider.call_count == 1

def test_find_text_targets_with_retry_success_after_retries(locator):
    """Test that it retries and succeeds if the target is found on a subsequent attempt."""
    mock_image_provider = MagicMock(return_value=b"fake_image_bytes")
    mock_target = UITarget(text="Submit", box=BoundingBox(x=0, y=0, width=10, height=10), center_x=5, center_y=5, confidence=95.0)
    
    # Return empty list for the first two calls, then the target on the third call
    with patch.object(locator, "find_text_targets", side_effect=[[], [], [mock_target]]) as mock_find:
        with patch("time.sleep") as mock_sleep:
            targets = locator.find_text_targets_with_retry(
                image_provider=mock_image_provider,
                search_text="Submit",
                max_attempts=3,
                retry_delay=0.1
            )
            
            assert len(targets) == 1
            assert targets[0].text == "Submit"
            assert mock_find.call_count == 3
            assert mock_image_provider.call_count == 3
            assert mock_sleep.call_count == 2  # Slept twice before succeeding

def test_find_text_targets_with_retry_fails_after_max_attempts(locator):
    """Test that it returns an empty list after exhausting all retry attempts."""
    mock_image_provider = MagicMock(return_value=b"fake_image_bytes")
    
    # Always return empty list
    with patch.object(locator, "find_text_targets", return_value=[]) as mock_find:
        with patch("time.sleep") as mock_sleep:
            targets = locator.find_text_targets_with_retry(
                image_provider=mock_image_provider,
                search_text="Submit",
                max_attempts=3,
                retry_delay=0.1
            )
            
            assert len(targets) == 0
            assert mock_find.call_count == 3
            assert mock_image_provider.call_count == 3
            assert mock_sleep.call_count == 2