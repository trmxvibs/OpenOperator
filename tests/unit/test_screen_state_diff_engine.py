"""
Unit tests for Screen State Diff Engine.

Following TDD, these tests define the expected behavior
before implementation.
"""

import pytest

from openoperator.perception.screen_state_analyzer import ScreenState
from openoperator.perception.screen_state_diff_engine import (
    ScreenStateDiffEngine,
)


@pytest.fixture
def engine() -> ScreenStateDiffEngine:
    return ScreenStateDiffEngine()


def test_no_change_detected(engine: ScreenStateDiffEngine) -> None:
    state1 = ScreenState(
        active_window="Notepad",
        visible_text="Hello World",
        raw_image=b"img1",
    )

    state2 = ScreenState(
        active_window="Notepad",
        visible_text="Hello World",
        raw_image=b"img2",
    )

    assert engine.has_changed(state1, state2) is False


def test_window_change_detected(engine: ScreenStateDiffEngine) -> None:
    state1 = ScreenState(
        active_window="Notepad",
        visible_text="Hello World",
        raw_image=b"img1",
    )

    state2 = ScreenState(
        active_window="Calculator",
        visible_text="Hello World",
        raw_image=b"img2",
    )

    assert engine.has_changed(state1, state2) is True


def test_text_change_detected(engine: ScreenStateDiffEngine) -> None:
    state1 = ScreenState(
        active_window="Notepad",
        visible_text="Hello",
        raw_image=b"img1",
    )

    state2 = ScreenState(
        active_window="Notepad",
        visible_text="Hello OpenOperator",
        raw_image=b"img2",
    )

    assert engine.has_changed(state1, state2) is True


def test_both_changed(engine: ScreenStateDiffEngine) -> None:
    state1 = ScreenState(
        active_window="Notepad",
        visible_text="Hello",
        raw_image=b"img1",
    )

    state2 = ScreenState(
        active_window="Chrome",
        visible_text="Google",
        raw_image=b"img2",
    )

    assert engine.has_changed(state1, state2) is True


def test_none_state_handling(engine: ScreenStateDiffEngine) -> None:
    state = ScreenState(
        active_window="Notepad",
        visible_text="Hello",
        raw_image=b"img",
    )

    assert engine.has_changed(None, state) is True
    assert engine.has_changed(state, None) is True


def test_both_none_states(engine: ScreenStateDiffEngine) -> None:
    assert engine.has_changed(None, None) is False


def test_whitespace_does_not_trigger_change(engine: ScreenStateDiffEngine) -> None:
    state1 = ScreenState(
        active_window="Notepad",
        visible_text="Hello World",
        raw_image=b"img1",
    )

    state2 = ScreenState(
        active_window="Notepad",
        visible_text="  Hello World  ",
        raw_image=b"img2",
    )

    assert engine.has_changed(state1, state2) is False