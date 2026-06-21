# D:\OpenOperator\src\openoperator\agent\screen_observation_loop.py

"""
Screen Observation Loop module for OpenOperator.

Provides the ScreenObservationLoop class, which iteratively perceives the screen state, 
plans actions based on that context, and executes them until a goal is achieved.
"""

import logging
from typing import Optional

from openoperator.agent.intent_parser import VisionIntentParser
from openoperator.agent.task_runner import TaskRunner
from openoperator.perception.ocr import OCREngine
from openoperator.perception.screenshot import ScreenshotEngine

logger = logging.getLogger(__name__)


class ScreenObservationLoop:
    """
    Orchestrates the continuous perception, planning, and execution loop.
    Iteratively captures the screen, feeds the context to the planner, 
    and hands the resulting steps to the runner.
    """

    def __init__(
        self,
        planner: Optional[VisionIntentParser] = None,
        runner: Optional[TaskRunner] = None,
        screenshot_engine: Optional[ScreenshotEngine] = None,
        ocr_engine: Optional[OCREngine] = None,
        max_iterations: int = 5,
    ) -> None:
        """
        Initializes the ScreenObservationLoop with perception, planning, and execution subsystems.

        Args:
            planner (Optional[VisionIntentParser]): The context-aware intent planner.
            runner (Optional[TaskRunner]): The task execution runner.
            screenshot_engine (Optional[ScreenshotEngine]): Engine to capture screen state.
            ocr_engine (Optional[OCREngine]): Engine to extract text from screenshots.
            max_iterations (int): The maximum number of perception-action loops before aborting.
        """
        # Placeholder for future context-aware planner if none is provided.
        # Currently using VisionIntentParser to satisfy dependency expectations, 
        # though parse_with_context must be implemented on the provided planner.
        self.planner = planner or VisionIntentParser()
        self.runner = runner or TaskRunner()
        self.screenshot_engine = screenshot_engine or ScreenshotEngine()
        self.ocr_engine = ocr_engine or OCREngine()
        self.max_iterations = max_iterations

    def run(self, goal: str) -> bool:
        """
        Executes the vision-guided observation loop.

        Args:
            goal (str): The natural language objective to achieve.

        Returns:
            bool: True if the goal is achieved, False if it fails or hits the iteration limit.
        """
        logger.info(f"Starting ScreenObservationLoop for goal: '{goal}' (Max Iterations: {self.max_iterations})")

        for iteration in range(1, self.max_iterations + 1):
            logger.info(f"--- ScreenObservationLoop Iteration {iteration} ---")
            
            logger.debug("Capturing screen state...")
            image = self.screenshot_engine.capture_screen()
            
            if not image:
                logger.error("ScreenObservationLoop aborted: Failed to capture screenshot.")
                return False

            logger.debug("Extracting OCR context...")
            screen_text = self.ocr_engine.extract_text(image)
            
            if not screen_text:
                logger.error("ScreenObservationLoop aborted: Failed to extract text from screen.")
                return False

            logger.debug("Requesting context-aware plan from planner...")
            
            # The planner must implement `parse_with_context` to handle the screen state.
            if not hasattr(self.planner, 'parse_with_context'):
                logger.error("ScreenObservationLoop aborted: Planner lacks 'parse_with_context' method.")
                return False
                
            plan = self.planner.parse_with_context(
                goal=goal,
                screen_context=screen_text,
            )

            if not plan.is_executable:
                logger.error("ScreenObservationLoop aborted: Planner generated a non-executable plan.")
                if hasattr(plan, 'missing_context') and plan.missing_context:
                    logger.error(f"Missing context: {', '.join(plan.missing_context)}")
                return False

            if len(plan.steps) == 0:
                logger.info("ScreenObservationLoop completed successfully: Goal achieved (0 steps required).")
                return True

            logger.debug(f"Executing plan with {len(plan.steps)} steps...")
            success = self.runner.execute_plan(plan)

            if not success:
                logger.error(f"ScreenObservationLoop aborted: Execution failed during iteration {iteration}.")
                return False

        logger.warning(f"ScreenObservationLoop aborted: Maximum iteration limit ({self.max_iterations}) reached.")
        return False