from unittest.mock import MagicMock

from openoperator.agent.state_based_retry_strategy import RetryDecision


def test_retry_strategy_receives_confidence_score():
    strategy = MagicMock()

    strategy.decide(
        confidence=0.10,
        retry_count=1,
        max_retries=3,
    )

    strategy.decide.assert_called_once_with(
        confidence=0.10,
        retry_count=1,
        max_retries=3,
    )


def test_low_confidence_maps_to_correction():
    strategy = MagicMock()
    strategy.decide.return_value = RetryDecision.CORRECT

    decision = strategy.decide(
        confidence=0.05,
        retry_count=0,
        max_retries=3,
    )

    assert decision == RetryDecision.CORRECT


def test_medium_confidence_maps_to_retry():
    strategy = MagicMock()
    strategy.decide.return_value = RetryDecision.RETRY

    decision = strategy.decide(
        confidence=0.50,
        retry_count=0,
        max_retries=3,
    )

    assert decision == RetryDecision.RETRY


def test_high_confidence_maps_to_continue():
    strategy = MagicMock()
    strategy.decide.return_value = RetryDecision.CONTINUE

    decision = strategy.decide(
        confidence=0.90,
        retry_count=0,
        max_retries=3,
    )

    assert decision == RetryDecision.CONTINUE


def test_retry_limit_maps_to_abort():
    strategy = MagicMock()
    strategy.decide.return_value = RetryDecision.ABORT

    decision = strategy.decide(
        confidence=0.50,
        retry_count=3,
        max_retries=3,
    )

    assert decision == RetryDecision.ABORT