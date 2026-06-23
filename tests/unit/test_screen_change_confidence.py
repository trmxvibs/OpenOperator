"""
Unit tests for Screen Change Confidence Scoring.
"""

import pytest

from openoperator.perception.screen_state_analyzer import ScreenState
from openoperator.perception.screen_state_diff_engine import (
    ScreenStateDiffEngine,
)


@pytest.fixture
def engine():
    return ScreenStateDiffEngine()


def test_identical_states_have_zero_confidence(engine):
    state1 = ScreenState(
        active_window="Notepad",
        visible_text="Hello World",
        raw_image=b"a",
    )

    state2 = ScreenState(
        active_window="Notepad",
        visible_text="Hello World",
        raw_image=b"b",
    )

    assert engine.change_confidence(state1, state2) == 0.0


def test_window_change_has_high_confidence(engine):
    state1 = ScreenState(
        active_window="Notepad",
        visible_text="Hello",
        raw_image=b"a",
    )

    state2 = ScreenState(
        active_window="Calculator",
        visible_text="Hello",
        raw_image=b"b",
    )

    confidence = engine.change_confidence(state1, state2)

    assert confidence >= 0.8


def test_small_text_change_has_nonzero_confidence(engine):
    state1 = ScreenState(
        active_window="Notepad",
        visible_text="Hello",
        raw_image=b"a",
    )

    state2 = ScreenState(
        active_window="Notepad",
        visible_text="Hello!",
        raw_image=b"b",
    )

    confidence = engine.change_confidence(state1, state2)

    assert confidence > 0.0
    assert confidence < 1.0


def test_large_text_change_has_higher_confidence(engine):
    state1 = ScreenState(
        active_window="Notepad",
        visible_text="Hello",
        raw_image=b"a",
    )

    state2 = ScreenState(
        active_window="Notepad",
        visible_text="Google Chrome New Tab OpenAI ChatGPT",
        raw_image=b"b",
    )

    confidence = engine.change_confidence(state1, state2)

    assert confidence > 0.4


def test_none_state_returns_full_confidence(engine):
    state = ScreenState(
        active_window="Notepad",
        visible_text="Hello",
        raw_image=b"a",
    )

    assert engine.change_confidence(None, state) == 1.0
    assert engine.change_confidence(state, None) == 1.0


def test_both_none_returns_zero_confidence(engine):
    assert engine.change_confidence(None, None) == 0.0


def test_confidence_always_between_zero_and_one(engine):
    state1 = ScreenState(
        active_window="A",
        visible_text="ABC",
        raw_image=b"a",
    )

    state2 = ScreenState(
        active_window="B",
        visible_text="XYZ",
        raw_image=b"b",
    )

    confidence = engine.change_confidence(state1, state2)

    assert 0.0 <= confidence <= 1.0