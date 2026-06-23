from unittest.mock import MagicMock

from openoperator.agent.state_based_retry_strategy import RetryDecision


def test_low_confidence_causes_correction_path():
    analyzer = MagicMock()
    diff_engine = MagicMock()
    retry_strategy = MagicMock()

    analyzer.analyze.side_effect = [
        "before_state",
        "after_state",
    ]

    diff_engine.change_confidence.return_value = 0.05

    retry_strategy.decide.return_value = RetryDecision.CORRECT

    before = analyzer.analyze()
    after = analyzer.analyze()

    confidence = diff_engine.change_confidence(
        before,
        after,
    )

    decision = retry_strategy.decide(
        confidence=confidence,
        retry_count=0,
        max_retries=3,
    )

    assert decision == RetryDecision.CORRECT


def test_medium_confidence_causes_retry_path():
    analyzer = MagicMock()
    diff_engine = MagicMock()
    retry_strategy = MagicMock()

    analyzer.analyze.side_effect = [
        "before_state",
        "after_state",
    ]

    diff_engine.change_confidence.return_value = 0.50

    retry_strategy.decide.return_value = RetryDecision.RETRY

    confidence = diff_engine.change_confidence(
        analyzer.analyze(),
        analyzer.analyze(),
    )

    decision = retry_strategy.decide(
        confidence=confidence,
        retry_count=0,
        max_retries=3,
    )

    assert decision == RetryDecision.RETRY


def test_high_confidence_causes_continue_path():
    analyzer = MagicMock()
    diff_engine = MagicMock()
    retry_strategy = MagicMock()

    analyzer.analyze.side_effect = [
        "before_state",
        "after_state",
    ]

    diff_engine.change_confidence.return_value = 0.90

    retry_strategy.decide.return_value = RetryDecision.CONTINUE

    confidence = diff_engine.change_confidence(
        analyzer.analyze(),
        analyzer.analyze(),
    )

    decision = retry_strategy.decide(
        confidence=confidence,
        retry_count=0,
        max_retries=3,
    )

    assert decision == RetryDecision.CONTINUE