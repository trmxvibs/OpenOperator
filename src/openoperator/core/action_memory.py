"""
Action memory module for OpenOperator.

This module provides an in-memory storage system to track the history
of actions taken by the agent during a task execution.
"""

from pydantic import BaseModel


class ActionRecord(BaseModel):
    """
    Structured data model representing a single executed action.
    
    Attributes:
        step (int): The sequential step number of the action.
        action (str): A description or string representation of the executed action.
        status (str): The outcome of the action (e.g., 'success', 'failed').
        timestamp (str): The ISO-8601 formatted timestamp of when the action occurred.
    """
    step: int
    action: str
    status: str
    timestamp: str


class ActionMemory:
    """
    In-memory storage system for tracking action history.
    """

    def __init__(self) -> None:
        """Initializes an empty action memory."""
        self._records: list[ActionRecord] = []

    def add_record(self, record: ActionRecord) -> None:
        """
        Adds a new action record to the memory.

        Args:
            record (ActionRecord): The action record to store.
        """
        self._records.append(record)

    def get_records(self) -> list[ActionRecord]:
        """
        Retrieves all stored action records.

        Returns:
            list[ActionRecord]: A copy of the list of all historical action records 
                                to prevent unintended external modification.
        """
        return self._records.copy()

    def clear(self) -> None:
        """
        Clears all stored action records from memory.
        """
        self._records.clear()