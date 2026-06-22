# D:\OpenOperator\tests\integration\test_notepad_workflow.py

"""
Integration test suite for validating OpenOperator against real Windows applications.

This module ensures that the core action controllers (Window, Keyboard) and 
perception engines (Screenshot, OCR, Verification) can successfully orchestrate 
a complete end-to-end workflow on a native desktop application.
"""

import subprocess
import sys
import time

import pytest

from openoperator.agent.task_runner import TaskRunner
from openoperator.agent.vision_models import VisionActionType, VisionStep, VisionTaskPlan

# Skip the entire test module if not running on Windows
pytestmark = pytest.mark.skipif(
    sys.platform != "win32", 
    reason="Notepad integration tests require a native Windows environment."
)


@pytest.fixture
def notepad_process():
    """
    Fixture to launch Notepad, yield the active process to the test, and ensure 
    it is forcefully cleaned up without saving changes, even if the test fails.
    """
    # 1. Launch Notepad using subprocess
    process = subprocess.Popen(["notepad.exe"])
    
    # 2. Wait for the Notepad window to fully initialize and render on the desktop
    time.sleep(2.0)
    
    yield process
    
    # 6. Close Notepad
    # 7. Do not save changes
    # Terminating the process on Windows safely kills it, bypassing the 
    # "Do you want to save changes?" UI dialog and leaving no hanging windows.
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=3.0)
        except subprocess.TimeoutExpired:
            process.kill()


def test_notepad_typing_workflow(notepad_process) -> None:
    """
    Validates the end-to-end OpenOperator execution pipeline against Notepad.
    
    Workflow:
    - Focuses the Notepad window using OS APIs.
    - Types a specific string using the keyboard controller.
    - Verifies the string was actually typed by capturing the screen and running OCR.
    """
    # Initialize the TaskRunner with all default production subsystems
    runner = TaskRunner()
    
    # Construct a deterministic execution plan for the integration workflow
    plan = VisionTaskPlan(
        original_prompt="Integration test: Type into Notepad and verify",
        is_executable=True,
        missing_context=[],
        steps=[
            # 3. Focus Notepad window
            VisionStep(
                step_id=1, 
                action_type=VisionActionType.FOCUS_WINDOW, 
                target_element="Notepad", 
                confidence=1.0
            ),
            # 4. Type specific text
            VisionStep(
                step_id=2, 
                action_type=VisionActionType.TYPE_TEXT, 
                input_data="Hello OpenOperator", 
                confidence=1.0
            ),
            # 5. Verify typing succeeded visually via OCR
            VisionStep(
                step_id=3, 
                action_type=VisionActionType.VERIFY_STATE, 
                input_data="Hello OpenOperator", 
                confidence=1.0
            )
        ]
    )
    
    # Execute the plan with a slight delay between OS actions to allow the UI to catch up
    success = runner.execute_plan(plan, delay_between_steps=1.5)
    
    # Assert the execution pipeline completed all steps successfully
    assert success is True, "OpenOperator failed to complete the Notepad integration workflow."