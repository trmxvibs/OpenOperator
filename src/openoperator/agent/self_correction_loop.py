"""
Self Correction Loop for OpenOperator.

Provides automatic recovery by:
1. Observing current screen state
2. Creating a plan
3. Executing the plan
4. Checking goal completion
5. Replanning if necessary
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class SelfCorrectionLoop:
    """
    Executes a goal using repeated observation,
    planning, execution, and verification cycles.
    """

    def __init__(
        self,
        observer: Optional[Any] = None,
        planner: Optional[Any] = None,
        executor: Optional[Any] = None,
        detector: Optional[Any] = None,
        max_retries: int = 3,
    ) -> None:

        self.observer = observer
        self.planner = planner
        self.executor = executor
        self.detector = detector
        self.max_retries = max_retries

    def run(self, goal: str) -> bool:
        """
        Execute goal with automatic recovery.
        """

        if (
            self.observer is None
            or self.planner is None
            or self.executor is None
            or self.detector is None
        ):
            logger.warning(
                "SelfCorrectionLoop initialized without dependencies."
            )
            return False

        for attempt in range(
            self.max_retries + 1
        ):
            logger.info(
                f"Self-correction attempt {attempt + 1}"
            )

            screen_state = (
                self.observer.observe()
            )

            plan = self.planner.create_plan(
                goal,
                screen_state,
            )

            execution_success = (
                self.executor.execute(
                    plan
                )
            )

            goal_completed = (
                self.detector.is_goal_completed(
                    goal,
                    screen_state,
                )
            )

            if (
                execution_success
                and goal_completed
            ):
                logger.info(
                    "Goal completed successfully."
                )
                return True

        logger.warning(
            "Maximum retry limit reached."
        )

        return False