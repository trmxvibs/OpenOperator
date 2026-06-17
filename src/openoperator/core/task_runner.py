# src/openoperator/core/task_runner.py

"""
Task runner module for OpenOperator.

This module provides the high-level orchestration for executing a user goal.
It combines planning, execution, memory tracking, and post-action verification.
"""

import logging
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel

from openoperator.agent.plan_executor import PlanExecutor
from openoperator.agent.task_planner import TaskPlan, TaskPlanner
from openoperator.core.action_memory import ActionMemory, ActionRecord
from openoperator.core.verification import VerificationEngine, VerificationResult
from openoperator.perception.ocr import OCREngine
from openoperator.perception.screenshot import ScreenshotEngine

logger = logging.getLogger(__name__)


class TaskResult(BaseModel):
    """
    Structured data model representing the complete outcome of a task run.
    """
    goal: str
    success: bool
    verification_reason: str
    action_history: list[ActionRecord]


class TaskRunner:
    """
    High-level orchestrator that executes a goal from end to end, tracking
    actions in memory and verifying the final screen state.
    """

    def __init__(
        self,
        planner: Optional[TaskPlanner] = None,
        executor: Optional[PlanExecutor] = None,
        memory: Optional[ActionMemory] = None,
        screenshot_engine: Optional[ScreenshotEngine] = None,
        ocr_engine: Optional[OCREngine] = None,
        verification_engine: Optional[VerificationEngine] = None,
    ) -> None:
        """
        Initializes the TaskRunner with required components. 
        Uses dependency injection with fallback to default instances.
        """
        self.planner = planner or TaskPlanner()
        self.executor = executor or PlanExecutor()
        self.memory = memory or ActionMemory()
        self.screenshot = screenshot_engine or ScreenshotEngine()
        self.ocr = ocr_engine or OCREngine()
        self.verification = verification_engine or VerificationEngine()

    def run(self, goal: str, expected_text: str) -> TaskResult:
        """
        Executes a user goal by generating a plan, executing actions sequentially,
        capturing the screen, and verifying the expected text presence.

        Args:
            goal (str): The natural language instruction for the agent.
            expected_text (str): The text expected to be visible on screen 
                                 after execution completes.

        Returns:
            TaskResult: The comprehensive result of the task execution.
        """
        logger.info(f"Starting TaskRunner for goal: '{goal}'")
        
        # 1. Clear previous memory for the new task
        self.memory.clear()

        # 2. Create Plan
        logger.info("Generating task plan...")
        plan = self.planner.create_plan(goal)
        
        if not plan.actions:
            logger.warning("Generated plan is empty. Aborting execution.")
            return TaskResult(
                goal=goal,
                success=False,
                verification_reason="Task aborted: No actionable steps could be planned.",
                action_history=[],
            )

        # 3. Execute Plan & Store Memory
        logger.info(f"Executing plan with {len(plan.actions)} actions...")
        for index, action in enumerate(plan.actions, start=1):
            # Create a single-step plan for the executor to maintain granular control
            step_plan = TaskPlan(goal=f"Execute step {index}", actions=[action])
            
            try:
                self.executor.execute(step_plan)
                status = "success"
            except Exception as e:
                logger.error(f"Execution failed at step {index}: {e}", exc_info=True)
                status = "failed"

            # Format the action description for memory storage
            action_desc = action.action
            if action.text:
                action_desc += f" '{action.text}'"
            elif action.x is not None and action.y is not None:
                action_desc += f" ({action.x}, {action.y})"

            # Store the action record
            record = ActionRecord(
                step=index,
                action=action_desc,
                status=status,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )
            self.memory.add_record(record)
            
            # Halt execution if a step fails
            if status == "failed":
                return TaskResult(
                    goal=goal,
                    success=False,
                    verification_reason=f"Task aborted: Execution failed at step {index}.",
                    action_history=self.memory.get_records(),
                )

        # 4. Capture Screen & Run OCR
        logger.info("Task execution complete. Capturing screen for verification...")
        image_bytes = self.screenshot.capture_screen()
        
        if not image_bytes:
            logger.error("Failed to capture screen.")
            return TaskResult(
                goal=goal,
                success=False,
                verification_reason="Verification failed: Screen capture returned empty bytes.",
                action_history=self.memory.get_records(),
            )

        logger.info("Extracting text via OCR...")
        screen_text = self.ocr.extract_text(image_bytes)

        # 5. Verify Expected Text
        logger.info(f"Verifying presence of expected text: '{expected_text}'")
        verification_result = self.verification.verify_text_present(
            expected_text=expected_text,
            screen_text=screen_text
        )

        logger.info(f"Task completion status: {verification_result.success}")

        return TaskResult(
            goal=goal,
            success=verification_result.success,
            verification_reason=verification_result.reason,
            action_history=self.memory.get_records(),
        )