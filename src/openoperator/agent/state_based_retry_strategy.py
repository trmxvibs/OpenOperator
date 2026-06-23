"""
State Based Retry Strategy.

Provides deterministic retry decisions based on:

- Screen change confidence
- Retry count
- Retry limits

No LLM dependency.
"""

from enum import Enum


class RetryDecision(str, Enum):
    """
    Possible retry decisions.
    """

    RETRY = "retry"
    CORRECT = "correct"
    CONTINUE = "continue"
    ABORT = "abort"


class StateBasedRetryStrategy:
    """
    Decides how the agent should react after an execution attempt.
    """

    def __init__(
        self,
        correction_threshold: float = 0.20,
        continue_threshold: float = 0.70,
    ) -> None:
        self.correction_threshold = correction_threshold
        self.continue_threshold = continue_threshold

    def decide(
        self,
        confidence: float,
        retry_count: int,
        max_retries: int,
    ) -> RetryDecision:
        """
        Returns a retry decision.

        Rules:

        retry_count >= max_retries
            -> ABORT

        confidence < correction_threshold
            -> CORRECT

        confidence >= continue_threshold
            -> CONTINUE

        otherwise
            -> RETRY
        """

        if retry_count >= max_retries:
            return RetryDecision.ABORT

        if confidence < self.correction_threshold:
            return RetryDecision.CORRECT

        if confidence >= self.continue_threshold:
            return RetryDecision.CONTINUE

        return RetryDecision.RETRY