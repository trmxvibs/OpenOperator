"""
Demonstration functions for OpenOperator components.

These functions provide standalone tests for the individual components
of the OpenOperator architecture.
"""

import logging
import time
from pathlib import Path

from openoperator.action.keyboard import KeyboardActionController
from openoperator.action.mouse import MouseActionController
from openoperator.perception.screenshot import ScreenshotEngine

logger = logging.getLogger(__name__)


def run_screenshot_demo() -> None:
    """
    Demonstrates capturing a screenshot using the ScreenshotEngine
    and saving it to the local disk.
    """
    logger.info("--- Running Screenshot Demo ---")
    engine = ScreenshotEngine()
    
    logger.info("Capturing screen...")
    image_bytes = engine.capture_screen()
    
    output_path = Path("demo_screenshot.png")
    output_path.write_bytes(image_bytes)
    
    logger.info(f"Screenshot successfully saved to {output_path.absolute()}")
    logger.info("Screenshot Demo complete.\n")


def run_mouse_demo() -> None:
    """
    Demonstrates basic mouse movements and clicking.
    """
    logger.info("--- Running Mouse Demo ---")
    mouse = MouseActionController()
    
    logger.info("Moving mouse to absolute coordinates (500, 500)...")
    mouse.move_mouse(500, 500)
    time.sleep(1.0)
    
    logger.info("Moving mouse to absolute coordinates (600, 500)...")
    mouse.move_mouse(600, 500)
    time.sleep(1.0)
    
    logger.info("Executing left click...")
    mouse.click("left")
    
    logger.info("Mouse Demo complete.\n")


def run_typing_demo() -> None:
    """
    Demonstrates simulating keyboard input.
    Provides a short delay for the user to focus a text input window.
    """
    logger.info("--- Running Typing Demo ---")
    keyboard = KeyboardActionController()
    
    logger.info("Starting in 3 seconds. Please focus on a text input window...")
    time.sleep(3.0)
    
    demo_text = "Hello from OpenOperator!"
    logger.info(f"Typing text: '{demo_text}'")
    keyboard.type_text(demo_text)
    
    logger.info("Typing Demo complete.\n")


def run_click_type_demo() -> None:
    """
    Demonstrates the combined usage of mouse and keyboard controllers
    to navigate to a location, click to focus, and type text.
    """
    logger.info("--- Running Click & Type Demo ---")
    mouse = MouseActionController()
    keyboard = KeyboardActionController()
    
    logger.info("Starting in 3 seconds. Please maximize your text editor...")
    time.sleep(3.0)
    
    logger.info("Moving mouse to center coordinates (500, 500)...")
    mouse.move_mouse(500, 500)
    time.sleep(0.5)
    
    logger.info("Executing left click to establish window focus...")
    mouse.click("left")
    time.sleep(0.5)
    
    demo_text = "OpenOperator automated click and type test successful."
    logger.info(f"Typing text: '{demo_text}'")
    keyboard.type_text(demo_text)
    
    logger.info("Click & Type Demo complete.\n")