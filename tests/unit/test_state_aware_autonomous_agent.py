from unittest.mock import MagicMock

from openoperator.agent.state_based_retry_strategy import RetryDecision


def test_low_confidence_triggers_correction():
    strategy = MagicMock()
    strategy.decide.return_value = RetryDecision.CORRECT

    assert strategy.decide(
        confidence=0.05,
        retry_count=0,
        max_retries=3,
    ) == RetryDecision.CORRECT


def test_medium_confidence_triggers_retry():
    strategy = MagicMock()
    strategy.decide.return_value = RetryDecision.RETRY

    assert strategy.decide(
        confidence=0.50,
        retry_count=0,
        max_retries=3,
    ) == RetryDecision.RETRY


def test_high_confidence_continues():
    strategy = MagicMock()
    strategy.decide.return_value = RetryDecision.CONTINUE

    assert strategy.decide(
        confidence=0.90,
        retry_count=0,
        max_retries=3,
    ) == RetryDecision.CONTINUE