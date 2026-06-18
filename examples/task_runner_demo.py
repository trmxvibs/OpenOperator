"""
Demonstration of the end-to-end NLP Vision Planning and Execution.

This script parses a natural language string into a VisionTaskPlan, 
then feeds it to the TaskRunner for dynamic physical execution.
"""

import logging
import subprocess
import sys
import time

from openoperator.agent.intent_parser import VisionIntentParser
from openoperator.agent.task_runner import TaskRunner


def main() -> None:
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    if sys.platform != "win32":
        logger.error("This demonstration requires a Windows operating system.")
        return

    logger.info("Initializing NLP Parser and TaskRunner...")
    parser = VisionIntentParser()
    runner = TaskRunner()

    # The natural language prompt driving the entire execution
    prompt = "Switch to Notepad then click File and type OpenOperator NLP Demo next verify Demo"
    
    logger.info(f"Natural Language Goal: '{prompt}'")
    logger.info("Parsing intent...")
    
    plan = parser.parse(prompt)

    if not plan.is_executable:
        logger.error(f"Cannot execute plan. Missing context: {plan.missing_context}")
        return

    # Print the parsed execution graph
    print("\n" + "=" * 50)
    print("COMPILED VISION TASK PLAN:")
    print("=" * 50)
    for step in plan.steps:
        print(f"Step {step.step_id}: {step.action_type.value}")
        if step.target_element:
            print(f"  Target: '{step.target_element}'")
        if step.input_data:
            print(f"  Data:   '{step.input_data}'")
    print("=" * 50 + "\n")

    logger.info("Launching Notepad for testing...")
    process = subprocess.Popen(["notepad.exe"])
    time.sleep(3.0)

    logger.info("Handing plan over to TaskRunner for execution...")
    
    # Executes the dynamic sequence based on the parsed NLP
    success = runner.execute_plan(plan, delay_between_steps=1.0)

    print("\n" + "=" * 50)
    print("EXECUTION RESULT")
    print("=" * 50)
    if success:
        print("STATUS: SUCCESS - All parsed NLP steps executed correctly.")
    else:
        print("STATUS: FAILED - Sequence aborted.")
    print("=" * 50 + "\n")

    logger.info("Cleaning up resources...")
    try:
        process.terminate()
    except Exception as e:
        logger.debug(f"Failed to terminate demo app: {e}")


if __name__ == "__main__":
    main()