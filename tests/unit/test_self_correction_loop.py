"""
Tests for SelfCorrectionLoop.

Defines expected behavior for automatic recovery and replanning
when execution fails before goal completion.
"""

from unittest.mock import Mock

import pytest

from openoperator.agent.self_correction_loop import SelfCorrectionLoop


@pytest.fixture
def mock_observer():
    return Mock()


@pytest.fixture
def mock_planner():
    return Mock()


@pytest.fixture
def mock_executor():
    return Mock()


@pytest.fixture
def mock_detector():
    return Mock()


def test_goal_completed_first_try(
    mock_observer,
    mock_planner,
    mock_executor,
    mock_detector,
):
    """
    Goal already achieved after first execution.
    """

    mock_observer.observe.return_value = "notepad open"

    mock_planner.create_plan.return_value = "plan"

    mock_executor.execute.return_value = True

    mock_detector.is_goal_completed.return_value = True

    loop = SelfCorrectionLoop(
        observer=mock_observer,
        planner=mock_planner,
        executor=mock_executor,
        detector=mock_detector,
    )

    assert loop.run("open notepad") is True


def test_recovery_after_single_failure(
    mock_observer,
    mock_planner,
    mock_executor,
    mock_detector,
):
    """
    First attempt fails.
    Second attempt succeeds.
    """

    mock_observer.observe.return_value = "screen"

    mock_planner.create_plan.return_value = "plan"

    mock_executor.execute.side_effect = [
        False,
        True,
    ]

    mock_detector.is_goal_completed.side_effect = [
        False,
        True,
    ]

    loop = SelfCorrectionLoop(
        observer=mock_observer,
        planner=mock_planner,
        executor=mock_executor,
        detector=mock_detector,
        max_retries=3,
    )

    assert loop.run("goal") is True


def test_max_retry_limit(
    mock_observer,
    mock_planner,
    mock_executor,
    mock_detector,
):
    """
    Agent should stop after max retries.
    """

    mock_observer.observe.return_value = "screen"

    mock_planner.create_plan.return_value = "plan"

    mock_executor.execute.return_value = False

    mock_detector.is_goal_completed.return_value = False

    loop = SelfCorrectionLoop(
        observer=mock_observer,
        planner=mock_planner,
        executor=mock_executor,
        detector=mock_detector,
        max_retries=3,
    )

    assert loop.run("goal") is False


def test_reobserve_after_failure(
    mock_observer,
    mock_planner,
    mock_executor,
    mock_detector,
):
    """
    Screen should be observed again after failure.
    """

    mock_observer.observe.side_effect = [
        "screen1",
        "screen2",
    ]

    mock_planner.create_plan.return_value = "plan"

    mock_executor.execute.side_effect = [
        False,
        True,
    ]

    mock_detector.is_goal_completed.side_effect = [
        False,
        True,
    ]

    loop = SelfCorrectionLoop(
        observer=mock_observer,
        planner=mock_planner,
        executor=mock_executor,
        detector=mock_detector,
    )

    loop.run("goal")

    assert mock_observer.observe.call_count >= 2


def test_backward_compatibility_defaults():
    """
    Object can be constructed with defaults.
    """

    loop = SelfCorrectionLoop()

    assert loop is not None