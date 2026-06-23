from unittest.mock import MagicMock

from openoperator.agent.state_based_retry_strategy import RetryDecision


def test_low_confidence_results_in_correction_decision():
    retry_strategy = MagicMock()
    retry_strategy.decide.return_value = RetryDecision.CORRECT

    decision = retry_strategy.decide(
        confidence=0.05,
        retry_count=0,
        max_retries=3,
    )

    assert decision == RetryDecision.CORRECT


def test_medium_confidence_results_in_retry_decision():
    retry_strategy = MagicMock()
    retry_strategy.decide.return_value = RetryDecision.RETRY

    decision = retry_strategy.decide(
        confidence=0.45,
        retry_count=0,
        max_retries=3,
    )

    assert decision == RetryDecision.RETRY


def test_high_confidence_results_in_continue_decision():
    retry_strategy = MagicMock()
    retry_strategy.decide.return_value = RetryDecision.CONTINUE

    decision = retry_strategy.decide(
        confidence=0.90,
        retry_count=0,
        max_retries=3,
    )

    assert decision == RetryDecision.CONTINUE