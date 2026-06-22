"""
Multi-Step Autonomous Executor for OpenOperator.

Coordinates repeated planning, execution,
and goal verification cycles until success
or maximum cycle limit is reached.
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class MultiStepAutonomousExecutor:
    """
    Executes a goal through multiple
    planning/execution cycles.
    """

    def __init__(
        self,
        planner: Optional[Any] = None,
        executor: Optional[Any] = None,
        detector: Optional[Any] = None,
        max_cycles: int = 5,
    ) -> None:

        self.planner = planner
        self.executor = executor
        self.detector = detector
        self.max_cycles = max_cycles

    def run(
        self,
        goal: str,
    ) -> bool:
        """
        Run until goal completion or cycle limit.
        """

        if (
            self.planner is None
            or self.executor is None
            or self.detector is None
        ):
            logger.warning(
                "MultiStepAutonomousExecutor initialized without dependencies."
            )
            return False

        for cycle in range(
            self.max_cycles
        ):
            logger.info(
                f"Autonomous cycle {cycle + 1}"
            )

            plan = self.planner.create_plan(
                goal
            )

            success = self.executor.execute(
                plan
            )

            if not success:
                logger.error(
                    "Execution failed."
                )
                return False

            completed = (
                self.detector.is_goal_completed(
                    goal
                )
            )

            if completed:
                logger.info(
                    "Goal completed."
                )
                return True

        logger.warning(
            "Maximum cycle limit reached."
        )

        return False