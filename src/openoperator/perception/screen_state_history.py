"""
Screen State History module.

Stores recent ScreenState snapshots for future
state comparison and autonomous reasoning.
"""

from collections import deque
from typing import Optional

from openoperator.perception.screen_state_analyzer import ScreenState


class ScreenStateHistory:

    def __init__(self, max_history: int = 10) -> None:
        self._history = deque(maxlen=max_history)

    def add(self, state: ScreenState) -> None:
        self._history.append(state)

    def latest(self) -> Optional[ScreenState]:
        if not self._history:
            return None

        return self._history[-1]

    def previous(self) -> Optional[ScreenState]:
        if len(self._history) < 2:
            return None

        return self._history[-2]

    def clear(self) -> None:
        self._history.clear()

    def size(self) -> int:
        return len(self._history)