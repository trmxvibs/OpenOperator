"""
Unit tests for the VisionTaskExecutor.

This test suite covers the end-to-end orchestration pipeline, ensuring that
success paths complete correctly and that any subsystem failure properly
aborts the execution sequence.
"""

from unittest.mock import MagicMock, patch

import pytest

from openoperator.agent.vision_task_executor import VisionTaskExecutor
from openoperator.core.verification import VerificationResult


@pytest.fixture(autouse=True)
def mock_sleep():
    """
    Autouse fixture to mock time.sleep across all tests in this module.
    Ensures tests run instantaneously without waiting for OS delays.
    """
    with patch("openoperator.agent.vision_task_executor.time.sleep") as mock:
        yield mock


@pytest.fixture
def mocks() -> dict[str, MagicMock]:
    """
    Provides a dictionary of pre-configured mock subsystems set to 
    return successful responses by default.
    """
    m = {
        "window": MagicMock(),
        "actor": MagicMock(),
        "keyboard": MagicMock(),
        "screenshot": MagicMock(),
        "ocr": MagicMock(),
        "verification": MagicMock()
    }
    
    # Configure default success states
    m["window"].focus_window_by_title.return_value = True
    m["actor"].click_text.return_value = True
    m["keyboard"].type_text.return_value = True
    m["screenshot"].capture_screen.return_value = b"fake_image_bytes"
    m["ocr"].extract_text.return_value = "fake extracted screen text"
    m["verification"].verify_text_present.return_value = VerificationResult(
        success=True, 
        reason="Expected text found."
    )
    
    return m


@pytest.fixture
def executor(mocks: dict[str, MagicMock]) -> VisionTaskExecutor:
    """
    Provides a VisionTaskExecutor instance injected with the mock subsystems.
    """
    return VisionTaskExecutor(
        window_controller=mocks["window"],
        vision_actor=mocks["actor"],
        keyboard_controller=mocks["keyboard"],
        screenshot_engine=mocks["screenshot"],
        ocr_engine=mocks["ocr"],
        verification_engine=mocks["verification"]
    )


def test_successful_execution(executor: VisionTaskExecutor, mocks: dict[str, MagicMock]) -> None:
    """Test that a fully successful sequence calls all dependencies with correct arguments."""
    result = executor.execute(
        window_title="Notepad",
        click_text="File",
        type_text="Hello World",
        verify_text="Hello World",
        delay_between_steps=0.0
    )

    assert result is True
    
    # Verify all subsystems were called sequentially with correct parameters
    mocks["window"].focus_window_by_title.assert_called_once_with("Notepad")
    mocks["actor"].click_text.assert_called_once_with("File")
    mocks["keyboard"].type_text.assert_called_once_with("Hello World")
    mocks["screenshot"].capture_screen.assert_called_once()
    mocks["ocr"].extract_text.assert_called_once_with(b"fake_image_bytes")
    mocks["verification"].verify_text_present.assert_called_once_with(
        expected_text="Hello World",
        screen_text="fake extracted screen text"
    )


def test_focus_failure_aborts_sequence(executor: VisionTaskExecutor, mocks: dict[str, MagicMock]) -> None:
    """Test that failing to focus the window immediately aborts the execution."""
    mocks["window"].focus_window_by_title.return_value = False

    result = executor.execute("Notepad", "File", "Hello", "Hello")

    assert result is False
    mocks["window"].focus_window_by_title.assert_called_once()
    # Sequence should abort here
    mocks["actor"].click_text.assert_not_called()
    mocks["keyboard"].type_text.assert_not_called()


def test_click_failure_aborts_sequence(executor: VisionTaskExecutor, mocks: dict[str, MagicMock]) -> None:
    """Test that failing to locate or click the target text aborts the execution."""
    mocks["actor"].click_text.return_value = False

    result = executor.execute("Notepad", "File", "Hello", "Hello")

    assert result is False
    mocks["window"].focus_window_by_title.assert_called_once()
    mocks["actor"].click_text.assert_called_once()
    # Sequence should abort here
    mocks["keyboard"].type_text.assert_not_called()


def test_typing_failure_aborts_sequence(executor: VisionTaskExecutor, mocks: dict[str, MagicMock]) -> None:
    """Test that a failure in the keyboard controller aborts the execution."""
    mocks["keyboard"].type_text.return_value = False

    result = executor.execute("Notepad", "File", "Hello", "Hello")

    assert result is False
    mocks["actor"].click_text.assert_called_once()
    mocks["keyboard"].type_text.assert_called_once()
    # Sequence should abort here
    mocks["screenshot"].capture_screen.assert_not_called()


def test_screenshot_failure_aborts_sequence(executor: VisionTaskExecutor, mocks: dict[str, MagicMock]) -> None:
    """Test that returning empty bytes from the screenshot engine aborts verification."""
    mocks["screenshot"].capture_screen.return_value = b""

    result = executor.execute("Notepad", "File", "Hello", "Hello")

    assert result is False
    mocks["keyboard"].type_text.assert_called_once()
    mocks["screenshot"].capture_screen.assert_called_once()
    # Sequence should abort here
    mocks["ocr"].extract_text.assert_not_called()


def test_ocr_failure_aborts_sequence(executor: VisionTaskExecutor, mocks: dict[str, MagicMock]) -> None:
    """Test that an empty OCR extraction aborts the verification step."""
    mocks["ocr"].extract_text.return_value = ""

    result = executor.execute("Notepad", "File", "Hello", "Hello")

    assert result is False
    mocks["screenshot"].capture_screen.assert_called_once()
    mocks["ocr"].extract_text.assert_called_once()
    # Sequence should abort here
    mocks["verification"].verify_text_present.assert_not_called()


def test_verification_failure_returns_false(executor: VisionTaskExecutor, mocks: dict[str, MagicMock]) -> None:
    """Test that an unsuccessful text verification correctly returns False."""
    mocks["verification"].verify_text_present.return_value = VerificationResult(
        success=False, 
        reason="Expected text missing."
    )

    result = executor.execute("Notepad", "File", "Hello", "Hello")

    assert result is False
    # All steps should have executed
    mocks["ocr"].extract_text.assert_called_once()
    mocks["verification"].verify_text_present.assert_called_once()