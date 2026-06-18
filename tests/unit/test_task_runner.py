"""
Unit tests for the TaskRunner executing VisionTaskPlans.
"""

from unittest.mock import MagicMock, patch

import pytest

from openoperator.agent.task_runner import TaskRunner
from openoperator.agent.vision_models import VisionActionType, VisionStep, VisionTaskPlan
from openoperator.core.verification import VerificationResult


@pytest.fixture(autouse=True)
def mock_sleep():
    """Mocks time.sleep to ensure tests run instantly."""
    with patch("openoperator.agent.task_runner.time.sleep") as mock:
        yield mock


@pytest.fixture
def mocks() -> dict[str, MagicMock]:
    """Provides pre-configured mock subsystems."""
    m = {
        "window": MagicMock(),
        "actor": MagicMock(),
        "keyboard": MagicMock(),
        "screenshot": MagicMock(),
        "ocr": MagicMock(),
        "verification": MagicMock()
    }
    
    m["window"].focus_window_by_title.return_value = True
    m["actor"].click_text.return_value = True
    m["keyboard"].type_text.return_value = True
    m["screenshot"].capture_screen.return_value = b"fake_bytes"
    m["ocr"].extract_text.return_value = "fake screen text"
    m["verification"].verify_text_present.return_value = VerificationResult(
        success=True, reason="Found"
    )
    
    return m


@pytest.fixture
def runner(mocks: dict[str, MagicMock]) -> TaskRunner:
    """Provides a TaskRunner injected with mocks."""
    return TaskRunner(
        window_controller=mocks["window"],
        vision_actor=mocks["actor"],
        keyboard_controller=mocks["keyboard"],
        screenshot_engine=mocks["screenshot"],
        ocr_engine=mocks["ocr"],
        verification_engine=mocks["verification"]
    )


@pytest.fixture
def valid_plan() -> VisionTaskPlan:
    """Provides a valid, end-to-end VisionTaskPlan."""
    return VisionTaskPlan(
        original_prompt="test prompt",
        is_executable=True,
        missing_context=[],
        steps=[
            VisionStep(step_id=1, action_type=VisionActionType.FOCUS_WINDOW, target_element="App", confidence=1.0),
            VisionStep(step_id=2, action_type=VisionActionType.CLICK_TEXT, target_element="Button", confidence=1.0),
            VisionStep(step_id=3, action_type=VisionActionType.TYPE_TEXT, input_data="Data", confidence=1.0),
            VisionStep(step_id=4, action_type=VisionActionType.VERIFY_STATE, input_data="Expected", confidence=1.0),
        ]
    )


def test_execute_plan_success(runner: TaskRunner, mocks: dict[str, MagicMock], valid_plan: VisionTaskPlan) -> None:
    """Test full pipeline success."""
    result = runner.execute_plan(valid_plan, delay_between_steps=0.0)

    assert result is True
    mocks["window"].focus_window_by_title.assert_called_once_with("App")
    mocks["actor"].click_text.assert_called_once_with("Button")
    mocks["keyboard"].type_text.assert_called_once_with("Data")
    mocks["screenshot"].capture_screen.assert_called_once()
    mocks["ocr"].extract_text.assert_called_once_with(b"fake_bytes")
    mocks["verification"].verify_text_present.assert_called_once_with(
        expected_text="Expected", screen_text="fake screen text"
    )


def test_execute_plan_not_executable(runner: TaskRunner, valid_plan: VisionTaskPlan) -> None:
    """Test rejection of non-executable plans."""
    valid_plan.is_executable = False
    result = runner.execute_plan(valid_plan)
    assert result is False


def test_focus_failure(runner: TaskRunner, mocks: dict[str, MagicMock], valid_plan: VisionTaskPlan) -> None:
    """Test sequence aborts on focus failure."""
    mocks["window"].focus_window_by_title.return_value = False
    result = runner.execute_plan(valid_plan)
    assert result is False
    mocks["actor"].click_text.assert_not_called()


def test_click_failure(runner: TaskRunner, mocks: dict[str, MagicMock], valid_plan: VisionTaskPlan) -> None:
    """Test sequence aborts on click failure."""
    mocks["actor"].click_text.return_value = False
    result = runner.execute_plan(valid_plan)
    assert result is False
    mocks["keyboard"].type_text.assert_not_called()


def test_typing_failure(runner: TaskRunner, mocks: dict[str, MagicMock], valid_plan: VisionTaskPlan) -> None:
    """Test sequence aborts on typing failure."""
    mocks["keyboard"].type_text.return_value = False
    result = runner.execute_plan(valid_plan)
    assert result is False
    mocks["verification"].verify_text_present.assert_not_called()


def test_verification_failure(runner: TaskRunner, mocks: dict[str, MagicMock], valid_plan: VisionTaskPlan) -> None:
    """Test verification correctly returns false on mismatch."""
    mocks["verification"].verify_text_present.return_value = VerificationResult(
        success=False, reason="Missing"
    )
    result = runner.execute_plan(valid_plan)
    assert result is False


def test_missing_required_data(runner: TaskRunner) -> None:
    """Test graceful failure if a step is missing required fields."""
    plan = VisionTaskPlan(
        original_prompt="bad",
        is_executable=True,
        missing_context=[],
        steps=[VisionStep(step_id=1, action_type=VisionActionType.TYPE_TEXT, input_data=None, confidence=1.0)]
    )
    assert runner.execute_plan(plan) is False