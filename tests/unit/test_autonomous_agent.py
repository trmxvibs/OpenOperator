# tests/unit/test_autonomous_agent.py

"""
Unit tests for the Autonomous Agent Orchestrator.

Following Test-Driven Development (TDD), these tests define the expected 
behavior of the upcoming AutonomousAgent class (Issue #50). The tests will fail 
until the implementation is completed.
"""

from unittest.mock import MagicMock, call

import pytest

# Expected future import
from openoperator.agent.autonomous_agent import AutonomousAgent


@pytest.fixture
def mocks() -> dict[str, MagicMock]:
    """Provides pre-configured mock subsystems for the AutonomousAgent."""
    return {
        "detector": MagicMock(),
        "executor": MagicMock(),
        "correction_loop": MagicMock(),
    }


@pytest.fixture
def autonomous_agent(mocks: dict[str, MagicMock]) -> AutonomousAgent:
    """Provides an AutonomousAgent injected with mocks and a strict retry limit."""
    # Expected API
    return AutonomousAgent(
        goal_detector=mocks["detector"],
        multi_step_executor=mocks["executor"],
        self_correction_loop=mocks["correction_loop"],
        max_retries=3
    )


def test_goal_already_completed(autonomous_agent: AutonomousAgent, mocks: dict[str, MagicMock]) -> None:
    """Test that if the goal is already met before execution, the agent returns True immediately."""
    mocks["detector"].is_goal_completed.return_value = True
    
    result = autonomous_agent.run("verify notepad is open")
    
    assert result is True
    mocks["detector"].is_goal_completed.assert_called_once_with("verify notepad is open")
    mocks["executor"].execute_autonomous_task.assert_not_called()
    mocks["correction_loop"].attempt_correction.assert_not_called()


def test_successful_first_execution(autonomous_agent: AutonomousAgent, mocks: dict[str, MagicMock]) -> None:
    """Test a standard execution where the executor succeeds on the first try."""
    # First check: goal not met. Second check (after execution): goal met.
    mocks["detector"].is_goal_completed.side_effect = [False, True]
    mocks["executor"].execute_autonomous_task.return_value = True
    
    result = autonomous_agent.run("open notepad")
    
    assert result is True
    assert mocks["detector"].is_goal_completed.call_count == 2
    mocks["executor"].execute_autonomous_task.assert_called_once_with("open notepad")
    mocks["correction_loop"].attempt_correction.assert_not_called()


def test_execution_fails_triggers_correction_and_retries(autonomous_agent: AutonomousAgent, mocks: dict[str, MagicMock]) -> None:
    """Test that an execution failure triggers the self-correction loop before retrying."""
    # Check 1: Goal not met
    # Execution 1: Fails
    # Correction 1: Succeeds (recovers state)
    # Check 2: Goal not met
    # Execution 2: Succeeds
    # Check 3: Goal met
    
    mocks["detector"].is_goal_completed.side_effect = [False, False, True]
    mocks["executor"].execute_autonomous_task.side_effect = [False, True]
    mocks["correction_loop"].attempt_correction.return_value = True
    
    result = autonomous_agent.run("click file")
    
    assert result is True
    assert mocks["executor"].execute_autonomous_task.call_count == 2
    mocks["correction_loop"].attempt_correction.assert_called_once()
    assert mocks["detector"].is_goal_completed.call_count == 3


def test_correction_fails_aborts_orchestration(autonomous_agent: AutonomousAgent, mocks: dict[str, MagicMock]) -> None:
    """Test that if the self-correction loop fails to recover, the agent aborts."""
    mocks["detector"].is_goal_completed.return_value = False
    mocks["executor"].execute_autonomous_task.return_value = False
    mocks["correction_loop"].attempt_correction.return_value = False  # Critical failure
    
    result = autonomous_agent.run("type hello")
    
    assert result is False
    mocks["executor"].execute_autonomous_task.assert_called_once()
    mocks["correction_loop"].attempt_correction.assert_called_once()
    assert mocks["detector"].is_goal_completed.call_count == 1  # Only checked before the first execution


def test_executor_succeeds_but_goal_not_met_triggers_correction(autonomous_agent: AutonomousAgent, mocks: dict[str, MagicMock]) -> None:
    """
    Test scenario where the task executor reports success (no crashing steps), 
    but the overarching goal is still not verified as complete. This should 
    also trigger the self-correction loop.
    """
    # Check 1: Not met. Check 2 (after exec): Not met. Check 3 (after correction & retry exec): Met.
    mocks["detector"].is_goal_completed.side_effect = [False, False, True]
    mocks["executor"].execute_autonomous_task.return_value = True # Claims it worked
    mocks["correction_loop"].attempt_correction.return_value = True
    
    result = autonomous_agent.run("open calculator")
    
    assert result is True
    assert mocks["executor"].execute_autonomous_task.call_count == 2
    mocks["correction_loop"].attempt_correction.assert_called_once()
    assert mocks["detector"].is_goal_completed.call_count == 3


def test_maximum_retries_exceeded(autonomous_agent: AutonomousAgent, mocks: dict[str, MagicMock]) -> None:
    """Test that the agent honors the maximum retry limit to prevent infinite loops."""
    mocks["detector"].is_goal_completed.return_value = False
    mocks["executor"].execute_autonomous_task.return_value = False
    mocks["correction_loop"].attempt_correction.return_value = True  # Always recovers, but execution always fails
    
    # Run a goal that never succeeds
    result = autonomous_agent.run("impossible goal")
    
    assert result is False
    # Max retries is 3. 
    # Initial attempt (1) + 3 retries = 4 executions total
    assert mocks["executor"].execute_autonomous_task.call_count == 4
    # Attempt correction happens after each failure (3 times)
    assert mocks["correction_loop"].attempt_correction.call_count == 3


def test_backward_compatibility_defaults() -> None:
    """Test that AutonomousAgent can initialize without explicitly provided mock dependencies."""
    try:
        # Expected to spin up default instances of its dependencies
        agent = AutonomousAgent()
        assert agent is not None
        assert agent.max_retries == 3 # Expected default
    except Exception as e:
        pytest.fail(f"AutonomousAgent failed to initialize with default parameters: {e}")