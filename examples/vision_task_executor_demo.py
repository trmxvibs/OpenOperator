"""
Demonstration of the end-to-end VisionTaskExecutor.

This script launches a test application (Notepad), waits a moment, 
and then orchestrates a full focus -> click -> type -> verify pipeline.
"""

import logging
import subprocess
import sys
import time

from openoperator.agent.vision_task_executor import VisionTaskExecutor


def main() -> None:
    # Configure logging for the demo
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    if sys.platform != "win32":
        logger.error("This demonstration requires a Windows operating system.")
        return

    logger.info("Initializing VisionTaskExecutor...")
    executor = VisionTaskExecutor()

    # Define the parameters for our test execution
    target_app_title = "Notepad"
    target_click_text = "File"  # Safe standard UI element to click to ensure window focus
    text_to_type = "OpenOperator Vision Task Execution Successful!"
    text_to_verify = "Vision Task Execution Successful"

    logger.info(f"Launching {target_app_title} for testing...")
    process = subprocess.Popen(["notepad.exe"])

    # Give the OS a moment to render the application completely
    logger.info("Waiting 3 seconds for the application to render...")
    time.sleep(3.0)

    # Scramble the user state slightly to prove it works
    logger.info("Executing sequence...")
    
    success = executor.execute(
        window_title=target_app_title,
        click_text=target_click_text,
        type_text=text_to_type,
        verify_text=text_to_verify,
        delay_between_steps=1.0
    )

    print("\n" + "=" * 50)
    print("TASK EXECUTION RESULT")
    print("=" * 50)
    if success:
        print("STATUS: SUCCESS")
        print("The agent successfully navigated the UI, typed the text, and verified it.")
    else:
        print("STATUS: FAILED")
        print("The sequence encountered an error or failed visual verification.")
    print("=" * 50 + "\n")

    logger.info("Cleaning up demo resources...")
    try:
        process.terminate()
        logger.info("Demo application closed.")
    except Exception as e:
        logger.debug(f"Could not terminate process: {e}")


if __name__ == "__main__":
    main()