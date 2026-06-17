"""
Task planner module for OpenOperator.

This module provides a rule-based MVP planner that parses natural language
goals and translates them into a structured sequence of actionable steps.
"""

import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class PlannedAction(BaseModel):
    """
    Structured data model representing a single deterministic action.
    """
    action: str
    x: int | None = None
    y: int | None = None
    text: str | None = None


class TaskPlan(BaseModel):
    """
    Structured data model representing a complete plan to achieve a goal.
    """
    goal: str
    actions: list[PlannedAction]


class TaskPlanner:
    """
    Rule-based task planner for OpenOperator MVP.

    Currently relies on keyword matching rather than an LLM/VLM to generate
    action sequences. Designed to be swapped with an AI-driven planner in
    future iterations.
    """

    def create_plan(self, goal: str) -> TaskPlan:
        """
        Creates a sequential task plan based on keyword detection in the goal string.

        Args:
            goal (str): The natural language instruction from the user.

        Returns:
            TaskPlan: A structured sequence of actions.
        """
        logger.debug(f"Creating rule-based plan for goal: '{goal}'")

        normalized_goal = goal.lower()
        actions: list[PlannedAction] = []

        # Move action
        if "move" in normalized_goal:
            logger.debug("Detected 'move' intent in goal.")
            actions.append(
                PlannedAction(
                    action="move",
                    x=0,
                    y=0,
                )
            )

        # Click action
        if "click" in normalized_goal:
            logger.debug("Detected 'click' intent in goal.")
            actions.append(
                PlannedAction(
                    action="click"
                )
            )

        # Type action
        if normalized_goal.startswith("type"):
            logger.debug("Detected 'type' intent in goal.")

            _, _, typed_text = goal.partition(" ")

            # Preserve original casing from user's goal.
            # Empty text is allowed and no longer replaced with a placeholder.
            extracted_text = typed_text.strip()

            actions.append(
                PlannedAction(
                    action="type",
                    text=extracted_text,
                )
            )

        if not actions:
            logger.warning(
                f"No supported action keywords ('move', 'click', 'type') "
                f"found in goal: '{goal}'. Plan will be empty."
            )

        logger.info(
            f"Successfully generated TaskPlan with {len(actions)} actions."
        )

        return TaskPlan(
            goal=goal,
            actions=actions,
        )
