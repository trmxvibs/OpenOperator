"""
Tests for MultiStepAutonomousExecutor.

This component coordinates:

Goal
→ Planning
→ Execution
→ Observation
→ Goal Detection

until the objective is achieved.
"""

from unittest.mock import Mock

from openoperator.agent.multi_step_autonomous_executor import (
    MultiStepAutonomousExecutor,
)


def test_goal_completed_after_single_cycle():
    planner = Mock()
    executor = Mock()
    detector = Mock()

    planner.create_plan.return_value = "plan"

    executor.execute.return_value = True

    detector.is_goal_completed.return_value = True

    autonomous = MultiStepAutonomousExecutor(
        planner=planner,
        executor=executor,
        detector=detector,
    )

    assert autonomous.run("open notepad") is True


def test_goal_completed_after_multiple_cycles():
    planner = Mock()
    executor = Mock()
    detector = Mock()

    planner.create_plan.return_value = "plan"

    executor.execute.return_value = True

    detector.is_goal_completed.side_effect = [
        False,
        False,
        True,
    ]

    autonomous = MultiStepAutonomousExecutor(
        planner=planner,
        executor=executor,
        detector=detector,
        max_cycles=5,
    )

    assert autonomous.run("goal") is True


def test_execution_failure_aborts():
    planner = Mock()
    executor = Mock()
    detector = Mock()

    planner.create_plan.return_value = "plan"

    executor.execute.return_value = False

    detector.is_goal_completed.return_value = False

    autonomous = MultiStepAutonomousExecutor(
        planner=planner,
        executor=executor,
        detector=detector,
    )

    assert autonomous.run("goal") is False


def test_maximum_cycle_limit():
    planner = Mock()
    executor = Mock()
    detector = Mock()

    planner.create_plan.return_value = "plan"

    executor.execute.return_value = True

    detector.is_goal_completed.return_value = False

    autonomous = MultiStepAutonomousExecutor(
        planner=planner,
        executor=executor,
        detector=detector,
        max_cycles=3,
    )

    assert autonomous.run("goal") is False


def test_backward_compatibility_defaults():
    autonomous = MultiStepAutonomousExecutor()

    assert autonomous is not None