"""
State-Aware Self Correction.

Uses ScreenStateAnalyzer,
ScreenStateHistory,
and ScreenStateDiffEngine
to determine whether corrective action
should be triggered.
"""

from typing import Optional

from openoperator.agent.self_correction_loop import SelfCorrectionLoop
from openoperator.perception.screen_state_analyzer import ScreenStateAnalyzer
from openoperator.perception.screen_state_history import ScreenStateHistory
from openoperator.perception.screen_state_diff_engine import (
    ScreenStateDiffEngine,
)


class StateAwareSelfCorrection:
    """
    Adds screen-state awareness on top of
    the existing SelfCorrectionLoop.
    """

    def __init__(
        self,
        analyzer: Optional[ScreenStateAnalyzer] = None,
        history: Optional[ScreenStateHistory] = None,
        diff_engine: Optional[ScreenStateDiffEngine] = None,
        correction_loop: Optional[SelfCorrectionLoop] = None,
    ) -> None:

        self.analyzer = analyzer or ScreenStateAnalyzer()
        self.history = history or ScreenStateHistory()
        self.diff_engine = diff_engine or ScreenStateDiffEngine()
        self.correction_loop = correction_loop or SelfCorrectionLoop()

    def evaluate(self) -> bool:
        """
        Analyze current state and determine
        whether correction is required.
        """

        current_state = self.analyzer.analyze()

        if current_state is None:
            return False

        previous_state = None

        if hasattr(self.history, "previous_state"):
            previous_state = self.history.previous_state()
        elif hasattr(self.history, "previous"):
            previous_state = self.history.previous()

        if hasattr(self.history, "add_state"):
            self.history.add_state(current_state)
        else:
            self.history.add(current_state)

        changed = self.diff_engine.has_changed(
            previous_state,
            current_state,
        )

        if changed:
            return True

        return self.correction_loop.attempt_correction()