"""
Goal-Oriented Agent Loop module for OpenOperator.

Provides the AgentLoop class, which iteratively plans and executes tasks
until a natural language goal is achieved, an error occurs, or the maximum
iteration limit is reached.
"""

import logging
from typing import Optional

from openoperator.agent.intent_parser import VisionIntentParser
from openoperator.agent.task_runner import TaskRunner

logger = logging.getLogger(__name__)


class AgentLoop:
    """
    Orchestrates the continuous planning and execution of a goal.
    Iteratively queries the planner for the next steps and hands them to the runner.
    """

    def __init__(
        self,
        planner: Optional[VisionIntentParser] = None,
        runner: Optional[TaskRunner] = None,
        max_iterations: int = 5,
    ) -> None:
        """
        Initializes the AgentLoop with a planner and an execution runner.

        Args:
            planner (Optional[VisionIntentParser]): The intent parser/planner to use.
            runner (Optional[TaskRunner]): The task execution runner to use.
            max_iterations (int): The maximum number of action loops before aborting.
        """
        self.planner = planner or VisionIntentParser()
        self.runner = runner or TaskRunner()
        self.max_iterations = max_iterations

    def run(self, goal: str) -> bool:
        """
        Executes the goal-oriented loop.

        Args:
            goal (str): The natural language objective to achieve.

        Returns:
            bool: True if the goal is achieved, False if it fails or hits the iteration limit.
        """
        logger.info(f"Starting AgentLoop for goal: '{goal}' (Max Iterations: {self.max_iterations})")

        for iteration in range(1, self.max_iterations + 1):
            logger.info(f"--- AgentLoop Iteration {iteration} ---")
            
            logger.debug("Requesting plan from planner...")
            plan = self.planner.parse(goal)

            if not plan.is_executable:
                logger.error("AgentLoop aborted: Planner generated a non-executable plan.")
                if hasattr(plan, 'missing_context') and plan.missing_context:
                    logger.error(f"Missing context: {', '.join(plan.missing_context)}")
                return False

            if len(plan.steps) == 0:
                logger.info("AgentLoop completed successfully: Goal achieved (0 steps required).")
                return True

            logger.debug(f"Executing plan with {len(plan.steps)} steps...")
            success = self.runner.execute_plan(plan)

            if not success:
                logger.error(f"AgentLoop aborted: Execution failed during iteration {iteration}.")
                return False

        logger.warning(f"AgentLoop aborted: Maximum iteration limit ({self.max_iterations}) reached.")
        return False