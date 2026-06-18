"""
Demonstration of the WindowController for OpenOperator.

This script opens an instance of Notepad, waits for the user to click away
or minimize it, and then programmatically pulls it back to the foreground.
"""

import logging
import subprocess
import sys
import time

from openoperator.action.window_controller import WindowController


def main() -> None:
    """Main execution point for the window focus demo."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    if sys.platform != "win32":
        logger.error("This demo requires a Windows operating system to run.")
        return

    logger.info("Initializing WindowController...")
    controller = WindowController()

    target_app = "Notepad"

    logger.info(f"Launching {target_app} to ensure a target exists...")
    # Open notepad without blocking the main script execution
    process = subprocess.Popen(["notepad.exe"])

    logger.info("\n--- ACTION REQUIRED ---")
    logger.info("Please click away, minimize Notepad, or open another window over it.")
    logger.info("Waiting 5 seconds before attempting to focus...\n")
    
    time.sleep(5.0)

    logger.info(f"Executing focus command for: '{target_app}'")
    success = controller.focus_window_by_title(target_app)

    print("\n" + "=" * 50)
    print("WINDOW FOCUS RESULT")
    print("=" * 50)
    if success:
        print(f"STATUS: SUCCESS - '{target_app}' should now be in the foreground.")
    else:
        print(f"STATUS: FAILED - Could not focus '{target_app}'.")
    print("=" * 50 + "\n")

    logger.info("Demo complete. Cleaning up...")
    
    # Clean up the notepad instance created specifically for the demo
    try:
        process.terminate()
        logger.info("Demo Notepad instance closed.")
    except Exception as e:
        logger.debug(f"Could not terminate Notepad: {e}")


if __name__ == "__main__":
    main()