# examples/task_runner_demo.py

"""
Demonstration of the end-to-end TaskRunner system.

This demo ties together the planner, executor, memory, and verification
engines to execute a natural language goal and evaluate its success.
"""

import logging
import time

from openoperator.core.task_runner import TaskRunner


def main() -> None:
    """
    Main entry point for the Task Runner demonstration.
    """
    # Configure root logging to output standard info messages
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    logger.info("Initializing TaskRunner with all subsystem dependencies...")
    runner = TaskRunner()

    goal = "type OpenOperator TaskRunner Demo"
    expected_text = "OpenOperator TaskRunner Demo"

    logger.info("Starting demo sequence in 5 seconds...")
    logger.info("Please focus your cursor on an empty text editor or input field.")
    time.sleep(5.0)

    logger.info(f"Executing Goal: '{goal}'")
    
    # Run the full orchestrated workflow
    result = runner.run(
        goal=goal,
        expected_text=expected_text
    )

    # Output the structured result payload
    print("\n" + "=" * 60)
    print("TASK RESULT JSON EXPORT:")
    print("=" * 60)
    print(result.model_dump_json(indent=4))
    print("=" * 60 + "\n")

    logger.info("TaskRunner demo complete.")


if __name__ == "__main__":
    main()