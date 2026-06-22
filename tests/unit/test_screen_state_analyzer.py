from unittest.mock import MagicMock

import pytest

from openoperator.perception.screen_state_analyzer import (
    ScreenState,
    ScreenStateAnalyzer,
)


@pytest.fixture
def mocks():
    return {
        "screenshot_engine": MagicMock(),
        "ocr_engine": MagicMock(),
        "window_controller": MagicMock(),
    }


@pytest.fixture
def analyzer(mocks):
    return ScreenStateAnalyzer(
        screenshot_engine=mocks["screenshot_engine"],
        ocr_engine=mocks["ocr_engine"],
        window_controller=mocks["window_controller"],
    )


def test_screen_state_creation(analyzer, mocks):
    mocks["screenshot_engine"].capture_screen.return_value = b"fake_image_bytes"
    mocks["ocr_engine"].extract_text.return_value = "File Edit View Help"
    mocks["window_controller"].get_active_window_title.return_value = "Notepad - Untitled"

    state = analyzer.analyze()

    assert isinstance(state, ScreenState)
    assert state.active_window == "Notepad - Untitled"
    assert state.visible_text == "File Edit View Help"
    assert state.raw_image == b"fake_image_bytes"


def test_active_window_extraction_failure(analyzer, mocks):
    mocks["screenshot_engine"].capture_screen.return_value = b"fake_image_bytes"
    mocks["ocr_engine"].extract_text.return_value = "Desktop icons"
    mocks["window_controller"].get_active_window_title.return_value = None

    state = analyzer.analyze()

    assert state.active_window is None
    assert state.visible_text == "Desktop icons"


def test_empty_ocr_handling(analyzer, mocks):
    mocks["screenshot_engine"].capture_screen.return_value = b"blank_image_bytes"
    mocks["ocr_engine"].extract_text.return_value = ""
    mocks["window_controller"].get_active_window_title.return_value = "Blank Window"

    state = analyzer.analyze()

    assert state.visible_text == ""
    assert state.active_window == "Blank Window"


def test_malformed_ocr_handling(analyzer, mocks):
    mocks["screenshot_engine"].capture_screen.return_value = b"corrupted_image_bytes"
    mocks["ocr_engine"].extract_text.side_effect = Exception("OCR Engine Crash")
    mocks["window_controller"].get_active_window_title.return_value = "Error Window"

    state = analyzer.analyze()

    assert state.visible_text == ""
    assert state.active_window == "Error Window"


def test_screenshot_capture_failure(analyzer, mocks):
    mocks["screenshot_engine"].capture_screen.return_value = None
    mocks["window_controller"].get_active_window_title.return_value = "Some Window"

    state = analyzer.analyze()

    assert state is None


def test_backward_compatibility_defaults():
    analyzer = ScreenStateAnalyzer()
    assert analyzer is not None