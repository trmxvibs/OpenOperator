"""
Visual Stasis Detector for OpenOperator.

Monitors the screen to detect when UI animations, loading screens, or 
transitions have finished. This prevents the agent from interacting 
prematurely with elements that are still rendering.
"""

import io
import logging
import time
from typing import Optional

from PIL import Image, ImageChops

from openoperator.perception.screenshot import ScreenshotEngine

logger = logging.getLogger(__name__)


class VisualStasisDetector:
    """
    Detects when the graphical interface has stopped moving/updating.
    """

    def __init__(self, screenshot_engine: Optional[ScreenshotEngine] = None) -> None:
        self.screenshot = screenshot_engine or ScreenshotEngine()

    def wait_for_stasis(
        self, 
        timeout: float = 10.0, 
        delay_between_checks: float = 0.5, 
        similarity_threshold: float = 0.99
    ) -> bool:
        """
        Blocks execution until the screen stops changing or the timeout is reached.

        Args:
            timeout (float): Maximum seconds to wait before giving up.
            delay_between_checks (float): Time to wait between taking screenshots.
            similarity_threshold (float): Percentage of pixels that must be identical (0.0 to 1.0).

        Returns:
            bool: True if stasis was achieved, False if it timed out.
        """
        logger.debug(f"Waiting for visual stasis (timeout={timeout}s)...")
        
        start_time = time.time()
        previous_image_bytes = self.screenshot.capture_screen()
        
        if not previous_image_bytes:
            logger.error("Failed to capture initial screen for stasis check.")
            return False

        while (time.time() - start_time) < timeout:
            time.sleep(delay_between_checks)
            current_image_bytes = self.screenshot.capture_screen()
            
            if not current_image_bytes:
                continue
                
            similarity = self._calculate_similarity(previous_image_bytes, current_image_bytes)
            
            if similarity >= similarity_threshold:
                logger.debug(f"Visual stasis achieved! (Similarity: {similarity:.2%})")
                return True
                
            logger.debug(f"Screen still changing. (Similarity: {similarity:.2%})")
            previous_image_bytes = current_image_bytes

        logger.warning("Visual stasis wait timed out. The screen might still be updating.")
        return False

    def _calculate_similarity(self, img1_bytes: bytes, img2_bytes: bytes) -> float:
        """
        Calculates the exact pixel similarity between two images.
        Uses Grayscale conversion and ImageChops for extreme performance.
        """
        try:
            # Convert to Grayscale ('L') to make comparison much faster
            img1 = Image.open(io.BytesIO(img1_bytes)).convert("L")
            img2 = Image.open(io.BytesIO(img2_bytes)).convert("L")
            
            # Find the difference between the two images
            diff = ImageChops.difference(img1, img2)
            
            # If no bounding box of difference exists, they are 100% identical
            if not diff.getbbox():
                return 1.0
                
            # diff.histogram() returns a list of counts for each pixel value (0-255).
            # Index 0 represents the count of completely identical pixels (difference of 0).
            histogram = diff.histogram()
            identical_pixels = histogram[0]
            total_pixels = img1.width * img1.height
            
            return identical_pixels / total_pixels
            
        except Exception as e:
            logger.error(f"Error calculating image similarity: {e}")
            return 0.0