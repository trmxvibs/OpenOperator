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

        if previous is None and current is None:
            return False

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

    def change_confidence(
        self,
        previous: Optional[ScreenState],
        current: Optional[ScreenState],
    ) -> float:
        """
        Returns a confidence score between 0.0 and 1.0
        representing how significant the change is.
        """

        if previous is None and current is None:
            return 0.0

        if previous is None or current is None:
            return 1.0

        score = 0.0

        previous_window = (previous.active_window or "").strip()
        current_window = (current.active_window or "").strip()

        if previous_window != current_window:
            score += 0.8

        previous_text = (previous.visible_text or "").strip()
        current_text = (current.visible_text or "").strip()

        if previous_text != current_text:
            max_len = max(
                len(previous_text),
                len(current_text),
                1,
            )

            length_diff = abs(
                len(previous_text) - len(current_text)
            )

            text_score = min(
                length_diff / max_len,
                1.0,
            )

            score += text_score * 0.5

        return min(score, 1.0)