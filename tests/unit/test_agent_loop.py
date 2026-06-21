"""
Unit tests for the Goal-Oriented Agent Loop.

Following Test-Driven Development (TDD), these tests define the expected 
behavior of the upcoming AgentLoop class. The tests will fail until the 
AgentLoop implementation is completed in Issue #35.
"""

from unittest.mock import MagicMock

import pytest

# Expected future import
from openoperator.agent.agent_loop import AgentLoop
from openoperator.agent.vision_models import VisionTaskPlan


@pytest.fixture
def mocks() -> dict[str, MagicMock]:
    """Provides pre-configured mock subsystems for the AgentLoop."""
    return {
        "planner": MagicMock(),
        "runner": MagicMock()
    }


@pytest.fixture
def agent_loop(mocks: dict[str, MagicMock]) -> AgentLoop:
    """Provides an AgentLoop injected with mocks and a strict iteration limit."""
    # Expected API: AgentLoop(planner, runner, max_iterations)
    return AgentLoop(
        planner=mocks["planner"],
        runner=mocks["runner"],
        max_iterations=3
    )


def test_goal_completed_immediately(agent_loop: AgentLoop, mocks: dict[str, MagicMock]) -> None:
    """
    Test that if the planner immediately determines no steps are needed,
    the loop completes successfully without invoking the executor.
    """
    empty_plan = MagicMock(spec=VisionTaskPlan)
    empty_plan.is_executable = True
    empty_plan.steps = []
    
    # The planner returns an empty executable plan (goal already met)
    mocks["planner"].parse.return_value = empty_plan
    
    result = agent_loop.run("verify notepad is open")
    
    assert result is True
    mocks["planner"].parse.assert_called_once_with("verify notepad is open")
    mocks["runner"].execute_plan.assert_not_called()


def test_goal_requires_multiple_iterations(agent_loop: AgentLoop, mocks: dict[str, MagicMock]) -> None:
    """
    Test that the loop can execute sequential plans until the planner 
    determines the goal is reached.
    """
    # Plan 1: Requires action
    plan1 = MagicMock(spec=VisionTaskPlan)
    plan1.is_executable = True
    plan1.steps = [1]
    
    # Plan 2: Requires action
    plan2 = MagicMock(spec=VisionTaskPlan)
    plan2.is_executable = True
    plan2.steps = [2]
    
    # Plan 3: Complete (no steps)
    plan_done = MagicMock(spec=VisionTaskPlan)
    plan_done.is_executable = True
    plan_done.steps = []
    
    # Simulate the planner adapting over 3 iterations
    mocks["planner"].parse.side_effect = [plan1, plan2, plan_done]
    mocks["runner"].execute_plan.return_value = True
    
    result = agent_loop.run("open notepad and type hello")
    
    assert result is True
    assert mocks["planner"].parse.call_count == 3
    assert mocks["runner"].execute_plan.call_count == 2


def test_maximum_iteration_limit_stops_execution(agent_loop: AgentLoop, mocks: dict[str, MagicMock]) -> None:
    """
    Test that an infinite loop is prevented if the goal is never reached 
    within the max_iterations limit.
    """
    infinite_plan = MagicMock(spec=VisionTaskPlan)
    infinite_plan.is_executable = True
    infinite_plan.steps = [1]
    
    # Planner always returns an actionable plan (never completes)
    mocks["planner"].parse.return_value = infinite_plan
    mocks["runner"].execute_plan.return_value = True
    
    result = agent_loop.run("impossible goal")
    
    # Should safely abort and return False after 3 iterations
    assert result is False
    assert mocks["planner"].parse.call_count == 3
    assert mocks["runner"].execute_plan.call_count == 3


def test_planner_failure_aborts_loop(agent_loop: AgentLoop, mocks: dict[str, MagicMock]) -> None:
    """
    Test that if the planner generates a non-executable plan (e.g., missing context),
    the loop safely aborts.
    """
    bad_plan = MagicMock(spec=VisionTaskPlan)
    bad_plan.is_executable = False
    bad_plan.missing_context = ["Need target window"]
    
    mocks["planner"].parse.return_value = bad_plan
    
    result = agent_loop.run("type hello")
    
    assert result is False
    mocks["planner"].parse.assert_called_once()
    mocks["runner"].execute_plan.assert_not_called()


def test_executor_failure_aborts_loop(agent_loop: AgentLoop, mocks: dict[str, MagicMock]) -> None:
    """
    Test that if the physical execution layer fails, the loop does not 
    blindly retry or continue.
    """
    valid_plan = MagicMock(spec=VisionTaskPlan)
    valid_plan.is_executable = True
    valid_plan.steps = [1]
    
    mocks["planner"].parse.return_value = valid_plan
    mocks["runner"].execute_plan.return_value = False  # Execution fails
    
    result = agent_loop.run("click File")
    
    assert result is False
    mocks["planner"].parse.assert_called_once()
    mocks["runner"].execute_plan.assert_called_once()


def test_backward_compatibility_defaults() -> None:
    """
    Test that AgentLoop can be instantiated with its default subsystems,
    requiring no explicit constructor arguments.
    """
    try:
        # Should initialize standard VisionIntentParser and TaskRunner internally
        loop = AgentLoop()
        assert loop is not None
    except Exception as e:
        pytest.fail(f"AgentLoop failed to initialize with default parameters: {e}")