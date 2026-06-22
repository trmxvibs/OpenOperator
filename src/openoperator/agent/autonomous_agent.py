"""
Autonomous Agent Orchestrator module for OpenOperator.

This module provides the AutonomousAgent class, which coordinates goal detection,
multi-step task execution, and self-correction to autonomously fulfill natural
language objectives.
"""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class _DefaultGoalDetector:
    """Lightweight default fallback for goal detection."""
    def is_goal_completed(self, goal: str) -> bool:
        logger.debug("Using default GoalDetector fallback (always returns False).")
        return False


class _DefaultMultiStepExecutor:
    """Lightweight default fallback for multi-step execution."""
    def execute_autonomous_task(self, goal: str) -> bool:
        logger.debug("Using default MultiStepExecutor fallback (always returns False).")
        return False


class _DefaultSelfCorrectionLoop:
    """Lightweight default fallback for self-correction."""
    def attempt_correction(self) -> bool:
        logger.debug("Using default SelfCorrectionLoop fallback (always returns False).")
        return False


class AutonomousAgent:
    """
    Autonomous Agent Orchestrator.
    
    Coordinates the high-level workflow of checking goals, executing tasks,
    and running self-correction loops when errors or incomplete states occur.
    """

    def __init__(
        self,
        goal_detector: Optional[Any] = None,
        multi_step_executor: Optional[Any] = None,
        self_correction_loop: Optional[Any] = None,
        max_retries: int = 3,
    ) -> None:
        """
        Initializes the AutonomousAgent with its required subsystems.
        Uses lightweight default implementations if none are provided to maintain
        backward compatibility.

        Args:
            goal_detector: Subsystem to verify if a goal is completed.
            multi_step_executor: Subsystem to execute the core task steps.
            self_correction_loop: Subsystem to recover from errors or stuck states.
            max_retries (int): Maximum number of retries after the initial attempt.
        """
        self.goal_detector = goal_detector or _DefaultGoalDetector()
        self.multi_step_executor = multi_step_executor or _DefaultMultiStepExecutor()
        self.self_correction_loop = self_correction_loop or _DefaultSelfCorrectionLoop()
        self.max_retries = max_retries

    def run(self, goal: str) -> bool:
        """
        Executes the autonomous orchestration loop for a given goal.

        Args:
            goal (str): The natural language objective to achieve.

        Returns:
            bool: True if the goal is successfully achieved, False otherwise.
        """
        logger.info(f"AutonomousAgent starting orchestration for goal: '{goal}'")

        # 1. Initial check: Is the goal already completed before we do anything?
        logger.debug("Evaluating if goal is completed prior to execution.")
        if self.goal_detector.is_goal_completed(goal):
            logger.info("Goal verified as completed. Exiting successfully.")
            return True

        # Total attempts = 1 initial execution + max_retries
        total_attempts = 1 + self.max_retries

        for attempt in range(1, total_attempts + 1):
            logger.info(f"--- Autonomous Execution Attempt {attempt}/{total_attempts} ---")

            # 2. Execute autonomous task
            logger.debug(f"Executing multi-step autonomous task for goal: '{goal}'")
            execution_success = self.multi_step_executor.execute_autonomous_task(goal)

            # 3. Verify actual goal completion if execution succeeds
            if execution_success:
                logger.debug("Execution reported success. Verifying actual goal completion.")
                if self.goal_detector.is_goal_completed(goal):
                    logger.info("Goal verified as completed. Orchestration successful.")
                    return True
                else:
                    logger.warning("Execution succeeded, but the goal is still not completed.")
            else:
                # 4. If execution fails
                logger.warning("Task execution failed during this attempt.")

            # 5 & 6. Self-correction and Retry logic
            if attempt < total_attempts:
                logger.info("Triggering self-correction loop before retrying.")
                correction_success = self.self_correction_loop.attempt_correction()
                
                if not correction_success:
                    logger.error("Self-correction failed. Aborting orchestration.")
                    return False
                
                # If execution failed, we check if the correction loop happened to resolve the goal
                # If execution succeeded (but goal wasn't met), we do NOT treat correction as completion 
                # and must re-attempt execution instead.
                if not execution_success:
                    logger.debug("Execution failed. Checking if self-correction resolved the goal.")
                    if self.goal_detector.is_goal_completed(goal):
                        logger.info("Goal verified as completed after correction. Exiting successfully.")
                        return True
            else:
                logger.warning(f"Maximum retries ({self.max_retries}) exhausted. Aborting.")

        logger.error("AutonomousAgent failed to complete the goal within the allowed attempts.")
        return False