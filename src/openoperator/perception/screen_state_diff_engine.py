"""
Screen State Diff Engine.

Compares two ScreenState snapshots and determines
whether the screen has meaningfully changed.
"""

from typing import Optional

from openoperator.perception.screen_state_analyzer import ScreenState


class ScreenStateDiffEngine:
    """
    Performs deterministic comparisons between
    ScreenState objects.
    """

    def has_changed(
        self,
        previous: Optional[ScreenState],
        current: Optional[ScreenState],
    ) -> bool:
        """
        Returns True if a meaningful screen change occurred.
        """

        # Both missing → no change
        if previous is None and current is None:
            return False

        # One missing → changed
        if previous is None or current is None:
            return True

        previous_window = previous.active_window or ""
        current_window = current.active_window or ""

        if previous_window != current_window:
            return True

        previous_text = (previous.visible_text or "").strip()
        current_text = (current.visible_text or "").strip()

        if previous_text != current_text:
            return True

        return False