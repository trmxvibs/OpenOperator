"""
Unit tests for State-Aware Self Correction.

Uses ScreenStateAnalyzer,
ScreenStateHistory,
and ScreenStateDiffEngine
to determine whether a corrective action
should be triggered.
"""

from unittest.mock import MagicMock

import pytest

from openoperator.agent.state_aware_self_correction import (
    StateAwareSelfCorrection,
)


@pytest.fixture
def mocks():
    return {
        "analyzer": MagicMock(),
        "history": MagicMock(),
        "diff_engine": MagicMock(),
        "correction_loop": MagicMock(),
    }


@pytest.fixture
def correction(mocks):
    return StateAwareSelfCorrection(
        analyzer=mocks["analyzer"],
        history=mocks["history"],
        diff_engine=mocks["diff_engine"],
        correction_loop=mocks["correction_loop"],
    )


def test_changed_screen_does_not_trigger_correction(
    correction,
    mocks,
):
    mocks["diff_engine"].has_changed.return_value = True

    result = correction.evaluate()

    assert result is True

    mocks["correction_loop"].attempt_correction.assert_not_called()


def test_unchanged_screen_triggers_correction(
    correction,
    mocks,
):
    mocks["diff_engine"].has_changed.return_value = False
    mocks["correction_loop"].attempt_correction.return_value = True

    result = correction.evaluate()

    assert result is True

    mocks["correction_loop"].attempt_correction.assert_called_once()


def test_correction_failure_propagates(
    correction,
    mocks,
):
    mocks["diff_engine"].has_changed.return_value = False
    mocks["correction_loop"].attempt_correction.return_value = False

    result = correction.evaluate()

    assert result is False


def test_analyzer_state_added_to_history(
    correction,
    mocks,
):
    fake_state = MagicMock()

    mocks["analyzer"].analyze.return_value = fake_state
    mocks["history"].previous_state.return_value = None

    correction.evaluate()

    mocks["history"].add_state.assert_called_once_with(fake_state)


def test_backward_compatibility_defaults():
    try:
        correction = StateAwareSelfCorrection()
        assert correction is not None
    except Exception as e:
        pytest.fail(
            f"Default initialization failed: {e}"
        )