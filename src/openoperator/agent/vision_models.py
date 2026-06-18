# src/openoperator/agent/vision_models.py

"""
Data models for Natural Language Vision Planning.

This module defines the structured data representations used by the intelligent
planning layer to translate unstructured natural language into actionable vision tasks.
"""

from enum import Enum

from pydantic import BaseModel


class VisionActionType(str, Enum):
    """
    Enumeration of supported vision-guided actions.
    """
    FOCUS_WINDOW = "FOCUS_WINDOW"
    CLICK_TEXT = "CLICK_TEXT"
    TYPE_TEXT = "TYPE_TEXT"
    VERIFY_STATE = "VERIFY_STATE"


class VisionStep(BaseModel):
    """
    Represents a single, atomic operation inferred from natural language.
    """
    step_id: int
    action_type: VisionActionType
    target_element: str | None = None
    input_data: str | None = None
    confidence: float


class VisionTaskPlan(BaseModel):
    """
    Represents a compiled sequence of vision steps intended to achieve a user's goal.
    """
    original_prompt: str
    steps: list[VisionStep]
    is_executable: bool
    missing_context: list[str]