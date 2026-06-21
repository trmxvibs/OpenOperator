"""
Unit tests for the Screen Observation Loop.

Following Test-Driven Development (TDD), these tests define the expected 
behavior of the upcoming ScreenObservationLoop class. The tests will fail 
until the implementation is completed in Issue #36.
"""

from unittest.mock import MagicMock

import pytest

# Expected future import
from openoperator.agent.screen_observation_loop import ScreenObservationLoop
from openoperator.agent.vision_models import VisionTaskPlan
from openoperator.core.verification import VerificationResult


@pytest.fixture
def mocks() -> dict[str, MagicMock]:
    """Provides pre-configured mock subsystems for the ScreenObservationLoop."""
    return {
        "planner": MagicMock(),
        "runner": MagicMock(),
        "screenshot": MagicMock(),
        "ocr": MagicMock(),
        "analysis": MagicMock()  # Future abstraction for higher-level screen state analysis
    }


@pytest.fixture
def observation_loop(mocks: dict[str, MagicMock]) -> ScreenObservationLoop:
    """Provides a ScreenObservationLoop injected with mocks and a strict iteration limit."""
    # Expected API
    return ScreenObservationLoop(
        planner=mocks["planner"],
        runner=mocks["runner"],
        screenshot_engine=mocks["screenshot"],
        ocr_engine=mocks["ocr"],
        max_iterations=3
    )


def test_capture_and_analyze_screen_before_planning(observation_loop: ScreenObservationLoop, mocks: dict[str, MagicMock]) -> None:
    """Test that the loop captures a screenshot and runs OCR before asking the planner for steps."""
    mocks["screenshot"].capture_screen.return_value = b"fake_image"
    mocks["ocr"].extract_text.return_value = "Extracted Screen Text"
    
    empty_plan = MagicMock(spec=VisionTaskPlan)
    empty_plan.is_executable = True
    empty_plan.steps = []
    mocks["planner"].parse_with_context.return_value = empty_plan
    
    result = observation_loop.run("check if notepad is open")
    
    assert result is True
    mocks["screenshot"].capture_screen.assert_called_once()
    mocks["ocr"].extract_text.assert_called_once_with(b"fake_image")
    # Expected new API for context-aware planner
    mocks["planner"].parse_with_context.assert_called_once_with(
        goal="check if notepad is open", 
        screen_context="Extracted Screen Text"
    )


def test_abort_if_screenshot_capture_fails(observation_loop: ScreenObservationLoop, mocks: dict[str, MagicMock]) -> None:
    """Test that the loop aborts immediately if it cannot perceive the screen visually."""
    mocks["screenshot"].capture_screen.return_value = None
    
    result = observation_loop.run("click start")
    
    assert result is False
    mocks["screenshot"].capture_screen.assert_called_once()
    mocks["ocr"].extract_text.assert_not_called()
    mocks["planner"].parse_with_context.assert_not_called()


def test_abort_if_screen_analysis_fails(observation_loop: ScreenObservationLoop, mocks: dict[str, MagicMock]) -> None:
    """Test that the loop aborts if OCR extraction fails (e.g., returns empty string)."""
    mocks["screenshot"].capture_screen.return_value = b"fake_image"
    mocks["ocr"].extract_text.return_value = ""  # Failed extraction
    
    result = observation_loop.run("click file")
    
    assert result is False
    mocks["screenshot"].capture_screen.assert_called_once()
    mocks["ocr"].extract_text.assert_called_once()
    mocks["planner"].parse_with_context.assert_not_called()


def test_re_observe_screen_after_execution(observation_loop: ScreenObservationLoop, mocks: dict[str, MagicMock]) -> None:
    """Test that the loop captures a new screenshot after a step is executed to evaluate progress."""
    mocks["screenshot"].capture_screen.return_value = b"fake_image"
    mocks["ocr"].extract_text.side_effect = ["State 1", "State 2"]
    
    # Iteration 1: Action required
    plan1 = MagicMock(spec=VisionTaskPlan)
    plan1.is_executable = True
    plan1.steps = [1]
    
    # Iteration 2: Goal achieved
    plan_done = MagicMock(spec=VisionTaskPlan)
    plan_done.is_executable = True
    plan_done.steps = []
    
    mocks["planner"].parse_with_context.side_effect = [plan1, plan_done]
    mocks["runner"].execute_plan.return_value = True
    
    result = observation_loop.run("open calc")
    
    assert result is True
    assert mocks["screenshot"].capture_screen.call_count == 2
    assert mocks["ocr"].extract_text.call_count == 2
    assert mocks["runner"].execute_plan.call_count == 1
    
    # Verify the planner received the updated state on the second pass
    mocks["planner"].parse_with_context.assert_called_with(
        goal="open calc", 
        screen_context="State 2"
    )


def test_maximum_iteration_limit_stops_execution(observation_loop: ScreenObservationLoop, mocks: dict[str, MagicMock]) -> None:
    """Test that an infinite loop is prevented if the goal is never reached."""
    mocks["screenshot"].capture_screen.return_value = b"fake_image"
    mocks["ocr"].extract_text.return_value = "Static State"
    
    infinite_plan = MagicMock(spec=VisionTaskPlan)
    infinite_plan.is_executable = True
    infinite_plan.steps = [1]
    
    mocks["planner"].parse_with_context.return_value = infinite_plan
    mocks["runner"].execute_plan.return_value = True
    
    result = observation_loop.run("impossible goal")
    
    assert result is False
    assert mocks["screenshot"].capture_screen.call_count == 3
    assert mocks["planner"].parse_with_context.call_count == 3
    assert mocks["runner"].execute_plan.call_count == 3


def test_backward_compatibility_defaults() -> None:
    """Test that ScreenObservationLoop initializes properly without explicit dependencies."""
    try:
        loop = ScreenObservationLoop()
        assert loop is not None
        assert loop.max_iterations == 5  # Default expected value
    except Exception as e:
        pytest.fail(f"ScreenObservationLoop failed to initialize with default parameters: {e}")