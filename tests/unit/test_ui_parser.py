"""
Tests for the Dynamic UI Parser.
"""

import io
from unittest.mock import patch

import pytest
from PIL import Image

from openoperator.perception.ui_parser import DynamicUIParser


@pytest.fixture
def dummy_image_bytes():
    """Generates a 10x10 dummy image in memory."""
    img = Image.new("RGB", (10, 10), color="white")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    return img_byte_arr.getvalue()


@patch("pytesseract.image_to_data")
def test_parse_ui_elements_success(mock_image_to_data, dummy_image_bytes):
    # Mocking tesseract dictionary output
    mock_image_to_data.return_value = {
        "text": ["", "Hello", " ", "World"],
        "conf": [0, 85, 0, 92],
        "left": [0, 10, 0, 50],
        "top": [0, 20, 0, 20],
        "width": [0, 40, 0, 45],
        "height": [0, 15, 0, 15],
    }

    parser = DynamicUIParser()
    elements = parser.parse_ui_elements(dummy_image_bytes, confidence_threshold=40)

    # Should ignore empty strings and low confidence items
    assert len(elements) == 2
    
    assert elements[0]["text"] == "Hello"
    assert elements[0]["bounds"]["left"] == 10
    assert elements[0]["confidence"] == 85

    assert elements[1]["text"] == "World"
    assert elements[1]["bounds"]["width"] == 45
    assert elements[1]["confidence"] == 92


@patch("pytesseract.image_to_data")
def test_parse_ui_elements_empty(mock_image_to_data, dummy_image_bytes):
    mock_image_to_data.return_value = {
        "text": ["", "   "],
        "conf": [0, 10],
        "left": [0, 0],
        "top": [0, 0],
        "width": [0, 0],
        "height": [0, 0],
    }

    parser = DynamicUIParser()
    elements = parser.parse_ui_elements(dummy_image_bytes)

    assert len(elements) == 0


def test_parse_ui_elements_invalid_image():
    parser = DynamicUIParser()
    elements = parser.parse_ui_elements(b"invalid_bytes")
    assert len(elements) == 0