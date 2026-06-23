from openoperator.agent.state_based_retry_strategy import (
    RetryDecision,
    StateBasedRetryStrategy,
)


def test_low_confidence_triggers_correction():
    strategy = StateBasedRetryStrategy()

    assert (
        strategy.decide(
            confidence=0.05,
            retry_count=0,
            max_retries=3,
        )
        == RetryDecision.CORRECT
    )


def test_medium_confidence_triggers_retry():
    strategy = StateBasedRetryStrategy()

    assert (
        strategy.decide(
            confidence=0.40,
            retry_count=0,
            max_retries=3,
        )
        == RetryDecision.RETRY
    )


def test_high_confidence_continues():
    strategy = StateBasedRetryStrategy()

    assert (
        strategy.decide(
            confidence=0.90,
            retry_count=0,
            max_retries=3,
        )
        == RetryDecision.CONTINUE
    )


def test_retry_limit_forces_abort():
    strategy = StateBasedRetryStrategy()

    assert (
        strategy.decide(
            confidence=0.50,
            retry_count=3,
            max_retries=3,
        )
        == RetryDecision.ABORT
    )


def test_confidence_boundary_values():
    strategy = StateBasedRetryStrategy()

    assert (
        strategy.decide(
            confidence=0.20,
            retry_count=0,
            max_retries=3,
        )
        == RetryDecision.RETRY
    )

    assert (
        strategy.decide(
            confidence=0.70,
            retry_count=0,
            max_retries=3,
        )
        == RetryDecision.CONTINUE
    )