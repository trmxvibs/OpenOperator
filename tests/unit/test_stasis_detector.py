"""
Tests for the Visual Stasis Detector.
Verifies that the agent can accurately detect UI stillness.
"""

import io
from unittest.mock import MagicMock

import pytest
from PIL import Image

from openoperator.perception.stasis_detector import VisualStasisDetector


def create_dummy_image(color="white") -> bytes:
    """Helper to generate an in-memory image."""
    img = Image.new("RGB", (100, 100), color=color)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    return img_bytes.getvalue()


@pytest.fixture
def mock_screenshot_engine():
    return MagicMock()


def test_calculate_similarity_identical():
    detector = VisualStasisDetector()
    img1 = create_dummy_image("white")
    img2 = create_dummy_image("white")
    
    similarity = detector._calculate_similarity(img1, img2)
    assert similarity == 1.0


def test_calculate_similarity_different():
    detector = VisualStasisDetector()
    img1 = create_dummy_image("white")
    img2 = create_dummy_image("black")
    
    similarity = detector._calculate_similarity(img1, img2)
    assert similarity < 1.0


def test_wait_for_stasis_immediate(mock_screenshot_engine):
    """Test when the screen is already stable."""
    # Engine returns the exact same image twice
    mock_screenshot_engine.capture_screen.side_effect = [
        create_dummy_image("white"),
        create_dummy_image("white")
    ]
    
    detector = VisualStasisDetector(screenshot_engine=mock_screenshot_engine)
    result = detector.wait_for_stasis(timeout=2.0, delay_between_checks=0.1)
    
    assert result is True
    assert mock_screenshot_engine.capture_screen.call_count == 2


def test_wait_for_stasis_timeout(mock_screenshot_engine):
    """Test when the screen keeps changing (e.g. infinite loader)."""
    # Engine keeps returning different images
    mock_screenshot_engine.capture_screen.side_effect = [
        create_dummy_image("white"),
        create_dummy_image("red"),
        create_dummy_image("blue"),
        create_dummy_image("green"),
        create_dummy_image("yellow")
    ]
    
    detector = VisualStasisDetector(screenshot_engine=mock_screenshot_engine)
    # Give it a very short timeout so it fails quickly
    result = detector.wait_for_stasis(timeout=0.25, delay_between_checks=0.1)
    
    assert result is False
    assert mock_screenshot_engine.capture_screen.call_count > 2