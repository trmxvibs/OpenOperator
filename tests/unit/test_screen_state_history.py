"""
Unit tests for Screen State History.

Following TDD, these tests define the expected behavior
of ScreenStateHistory before implementation.
"""

import pytest

from openoperator.perception.screen_state_analyzer import ScreenState
from openoperator.perception.screen_state_history import ScreenStateHistory


@pytest.fixture
def history() -> ScreenStateHistory:
    return ScreenStateHistory(max_history=3)


def test_add_single_state(history: ScreenStateHistory) -> None:
    state = ScreenState(
        active_window="Notepad",
        visible_text="Hello",
        raw_image=b"img1"
    )

    history.add(state)

    assert history.size() == 1
    assert history.latest() == state


def test_add_multiple_states(history: ScreenStateHistory) -> None:
    state1 = ScreenState("A", "Text A", b"a")
    state2 = ScreenState("B", "Text B", b"b")

    history.add(state1)
    history.add(state2)

    assert history.size() == 2
    assert history.latest() == state2
    assert history.previous() == state1


def test_max_history_limit(history: ScreenStateHistory) -> None:
    history.add(ScreenState("1", "", b"1"))
    history.add(ScreenState("2", "", b"2"))
    history.add(ScreenState("3", "", b"3"))
    history.add(ScreenState("4", "", b"4"))

    assert history.size() == 3

    assert history.latest().active_window == "4"
    assert history.previous().active_window == "3"


def test_previous_without_enough_history(history: ScreenStateHistory) -> None:
    history.add(ScreenState("Only", "", b"x"))

    assert history.previous() is None


def test_clear_history(history: ScreenStateHistory) -> None:
    history.add(ScreenState("A", "", b"a"))
    history.add(ScreenState("B", "", b"b"))

    history.clear()

    assert history.size() == 0
    assert history.latest() is None


def test_empty_history(history: ScreenStateHistory) -> None:
    assert history.latest() is None
    assert history.previous() is None
    assert history.size() == 0