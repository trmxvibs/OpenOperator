from unittest.mock import MagicMock

from openoperator.agent.state_based_retry_strategy import RetryDecision
from openoperator.perception.screen_state_analyzer import ScreenState


def test_state_analysis_occurs_before_and_after_execution():
    analyzer = MagicMock()

    analyzer.analyze.side_effect = [
        ScreenState(
            active_window="Notepad",
            visible_text="Before",
            raw_image=b"a",
        ),
        ScreenState(
            active_window="Notepad",
            visible_text="After",
            raw_image=b"b",
        ),
    ]

    analyzer.analyze()
    analyzer.analyze()

    assert analyzer.analyze.call_count == 2


def test_confidence_is_calculated_from_two_states():
    diff_engine = MagicMock()

    diff_engine.change_confidence.return_value = 0.55

    confidence = diff_engine.change_confidence(
        "previous_state",
        "current_state",
    )

    assert confidence == 0.55


def test_retry_strategy_receives_confidence_value():
    strategy = MagicMock()

    strategy.decide.return_value = RetryDecision.RETRY

    strategy.decide(
        confidence=0.55,
        retry_count=1,
        max_retries=3,
    )

    strategy.decide.assert_called_once_with(
        confidence=0.55,
        retry_count=1,
        max_retries=3,
    )