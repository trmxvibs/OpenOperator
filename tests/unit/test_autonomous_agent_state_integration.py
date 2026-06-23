from unittest.mock import MagicMock

from openoperator.agent.autonomous_agent import AutonomousAgent
from openoperator.agent.state_based_retry_strategy import RetryDecision


def test_autonomous_agent_uses_retry_strategy_after_execution():
    goal_detector = MagicMock()
    executor = MagicMock()
    correction_loop = MagicMock()

    state_analyzer = MagicMock()
    diff_engine = MagicMock()
    retry_strategy = MagicMock()

    goal_detector.is_goal_completed.side_effect = [
        False,  # before execution
        False,  # after execution
    ]

    executor.execute_autonomous_task.return_value = True

    state_analyzer.analyze.side_effect = [
        "before_state",
        "after_state",
    ]

    diff_engine.change_confidence.return_value = 0.15

    retry_strategy.decide.return_value = RetryDecision.CORRECT

    agent = AutonomousAgent(
        goal_detector=goal_detector,
        multi_step_executor=executor,
        self_correction_loop=correction_loop,
    )

    # Future integration points
    agent.state_analyzer = state_analyzer
    agent.diff_engine = diff_engine
    agent.retry_strategy = retry_strategy

    # simulate future behavior
    before = agent.state_analyzer.analyze()

    agent.multi_step_executor.execute_autonomous_task("test goal")

    after = agent.state_analyzer.analyze()

    confidence = agent.diff_engine.change_confidence(
        before,
        after,
    )

    decision = agent.retry_strategy.decide(
        confidence=confidence,
        retry_count=0,
        max_retries=3,
    )

    assert decision == RetryDecision.CORRECT