"""
Unit tests for Memory-Aware Task Execution.

This test suite verifies that the TaskRunner properly updates the 
ActionMemoryManager during successful executions, preserves memory 
during failures, and maintains backward compatibility if no memory 
manager is injected.
"""

from unittest.mock import MagicMock, patch

import pytest

from openoperator.agent.action_memory_manager import ActionMemoryManager
from openoperator.agent.task_runner import TaskRunner
from openoperator.agent.vision_models import VisionActionType, VisionStep, VisionTaskPlan


@pytest.fixture(autouse=True)
def mock_sleep():
    """Mocks time.sleep to ensure tests run instantly."""
    with patch("openoperator.agent.task_runner.time.sleep") as mock:
        yield mock


@pytest.fixture
def mocks() -> dict[str, MagicMock]:
    """Provides pre-configured mock subsystems set to succeed by default."""
    m = {
        "window": MagicMock(),
        "actor": MagicMock(),
        "keyboard": MagicMock(),
        "screenshot": MagicMock(),
        "ocr": MagicMock(),
        "verification": MagicMock()
    }
    
    m["window"].focus_window_by_title.return_value = True
    m["actor"].click_text.return_value = True
    m["keyboard"].type_text.return_value = True
    
    return m


@pytest.fixture
def memory() -> ActionMemoryManager:
    """Provides a fresh ActionMemoryManager."""
    return ActionMemoryManager()


@pytest.fixture
def runner_with_memory(mocks: dict[str, MagicMock], memory: ActionMemoryManager) -> TaskRunner:
    """Provides a TaskRunner injected with mocks and a memory manager."""
    return TaskRunner(
        window_controller=mocks["window"],
        vision_actor=mocks["actor"],
        keyboard_controller=mocks["keyboard"],
        action_memory_manager=memory
    )


@pytest.fixture
def runner_without_memory(mocks: dict[str, MagicMock]) -> TaskRunner:
    """Provides a TaskRunner injected with mocks but NO memory manager."""
    # Simulates backward compatibility instantiation
    runner = TaskRunner(
        window_controller=mocks["window"],
        vision_actor=mocks["actor"],
        keyboard_controller=mocks["keyboard"]
    )
    # Force memory to None if it defaults to a new instance in the constructor
    # (depending on the exact TaskRunner implementation, to ensure strict testing).
    runner.memory = None 
    return runner


def test_successful_focus_updates_memory(runner_with_memory: TaskRunner, memory: ActionMemoryManager) -> None:
    """Test that a successful FOCUS_WINDOW action stores the window name in memory."""
    plan = VisionTaskPlan(
        original_prompt="open notepad",
        is_executable=True,
        missing_context=[],
        steps=[
            VisionStep(step_id=1, action_type=VisionActionType.FOCUS_WINDOW, target_element="Notepad", confidence=1.0)
        ]
    )
    
    success = runner_with_memory.execute_plan(plan)
    
    assert success is True
    assert memory.last_window == "Notepad"


def test_successful_click_updates_memory(runner_with_memory: TaskRunner, memory: ActionMemoryManager) -> None:
    """Test that a successful CLICK_TEXT action stores the target in memory."""
    plan = VisionTaskPlan(
        original_prompt="click File",
        is_executable=True,
        missing_context=[],
        steps=[
            VisionStep(step_id=1, action_type=VisionActionType.CLICK_TEXT, target_element="File", confidence=1.0)
        ]
    )
    
    success = runner_with_memory.execute_plan(plan)
    
    assert success is True
    assert memory.last_click == "File"


def test_successful_typing_updates_memory(runner_with_memory: TaskRunner, memory: ActionMemoryManager) -> None:
    """Test that a successful TYPE_TEXT action stores the input data in memory."""
    plan = VisionTaskPlan(
        original_prompt="type Hello",
        is_executable=True,
        missing_context=[],
        steps=[
            VisionStep(step_id=1, action_type=VisionActionType.TYPE_TEXT, input_data="Hello", confidence=1.0)
        ]
    )
    
    success = runner_with_memory.execute_plan(plan)
    
    assert success is True
    assert memory.last_typed == "Hello"


def test_execution_failure_preserves_previous_memory(
    runner_with_memory: TaskRunner, 
    memory: ActionMemoryManager, 
    mocks: dict[str, MagicMock]
) -> None:
    """Test that an action failure does not overwrite or corrupt previously stored valid memory."""
    
    # Setup pre-existing valid memory
    memory.remember_window("Chrome")
    memory.remember_click("Search")
    
    # Configure the keyboard controller to FAIL on the next typing step
    mocks["keyboard"].type_text.return_value = False
    
    plan = VisionTaskPlan(
        original_prompt="type OpenOperator",
        is_executable=True,
        missing_context=[],
        steps=[
            VisionStep(step_id=1, action_type=VisionActionType.TYPE_TEXT, input_data="OpenOperator", confidence=1.0)
        ]
    )
    
    success = runner_with_memory.execute_plan(plan)
    
    # Execution should fail, and memory should remain intact without the failed typed string
    assert success is False
    assert memory.last_window == "Chrome"
    assert memory.last_click == "Search"
    assert memory.last_typed is None


def test_backward_compatibility_no_memory(runner_without_memory: TaskRunner) -> None:
    """
    Test that the TaskRunner executes successfully without crashing 
    when no memory manager is configured (backward compatibility).
    """
    plan = VisionTaskPlan(
        original_prompt="open notepad and click file",
        is_executable=True,
        missing_context=[],
        steps=[
            VisionStep(step_id=1, action_type=VisionActionType.FOCUS_WINDOW, target_element="Notepad", confidence=1.0),
            VisionStep(step_id=2, action_type=VisionActionType.CLICK_TEXT, target_element="File", confidence=1.0)
        ]
    )
    
    # If the implementation has a strict dependency failure, this will crash.
    # It should gracefully ignore memory recording if memory is None.
    success = runner_without_memory.execute_plan(plan)
    
    assert success is True