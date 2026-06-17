# src/openoperator/core/verification.py

"""
Verification engine module for OpenOperator.

This module provides mechanisms to verify the state of the screen
against expected outcomes to confirm task success or failure.
"""

import logging

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class VerificationResult(BaseModel):
    """
    Structured data model representing the outcome of a verification check.
    """
    success: bool
    reason: str


class VerificationEngine:
    """
    Engine responsible for verifying system state against expected conditions.
    """

    def verify_text_present(self, expected_text: str, screen_text: str) -> VerificationResult:
        """
        Verifies if the expected text is present within the parsed screen text.

        Performs a case-insensitive, whitespace-trimmed substring search.

        Args:
            expected_text (str): The specific string expected to be on the screen.
            screen_text (str): The full raw text extracted from the screen via OCR.

        Returns:
            VerificationResult: An object containing the boolean success state
                                and a descriptive reason for the result.
        """
        logger.debug(f"Verifying presence of text: '{expected_text}'")

        if not expected_text:
            msg = "Expected text was empty. Cannot verify presence."
            logger.warning(msg)
            return VerificationResult(
                success=False,
                reason=msg
            )

        clean_expected = expected_text.strip().lower()
        clean_screen = screen_text.strip().lower()

        if clean_expected in clean_screen:
            reason = f"Successfully found expected text: '{expected_text}'"
            logger.info(reason)
            return VerificationResult(success=True, reason=reason)
        else:
            reason = f"Expected text '{expected_text}' was not found on the screen."
            logger.info(reason)
            return VerificationResult(success=False, reason=reason)