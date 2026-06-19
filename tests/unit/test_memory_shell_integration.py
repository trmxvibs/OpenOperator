"""
Integration tests for the Interactive Shell and Action Memory subsystem.

Ensures that executing commands updates the memory state properly 
and that the 'memory' command outputs the correct context.
"""

from unittest.mock import MagicMock, patch
import pytest

from openoperator.agent.action_memory_manager import ActionMemoryManager
from openoperator.agent.task_runner import TaskRunner
from openoperator.agent.vision_models import VisionActionType, VisionStep, VisionTaskPlan
from openoperator.shell import InteractiveShell


@pytest.fixture
def memory() -> ActionMemoryManager:
    """Provides a fresh ActionMemoryManager."""
    return ActionMemoryManager()


@pytest.fixture
def shell_with_mocks(memory: ActionMemoryManager) -> InteractiveShell:
    """Provides a shell with a mock parser and heavily mocked runner to prevent OS side-effects."""
    runner = TaskRunner(action_memory_manager=memory)
    
    # Mock hardware and vision controllers to always succeed
    runner.window.focus_window_by_title = MagicMock(return_value=True)
    runner.actor.click_text = MagicMock(return_value=True)
    runner.keyboard.type_text = MagicMock(return_value=True)
    runner.screenshot.capture_screen = MagicMock(return_value=b"fake_bytes")
    runner.ocr.extract_text = MagicMock(return_value="fake text")
    
    verify_mock = MagicMock()
    verify_mock.success = True
    runner.verification.verify_text_present = MagicMock(return_value=verify_mock)

    parser = MagicMock()
    return InteractiveShell(parser=parser, runner=runner)


def test_memory_command_empty_state(shell_with_mocks: InteractiveShell, capsys: pytest.CaptureFixture) -> None:
    """Test that the memory command outputs 'None' when the state is empty."""
    with patch('builtins.input', side_effect=['memory', 'exit']):
        shell_with_mocks.cmdloop()
        
    captured = capsys.readouterr().out
    
    assert "Current Session Memory" in captured
    assert "Last Window: None" in captured
    assert "Last Click: None" in captured
    assert "Last Typed: None" in captured


def test_memory_updates_after_actions(shell_with_mocks: InteractiveShell, capsys: pytest.CaptureFixture) -> None:
    """Test that successfully executing a plan updates the memory and displays it correctly."""
    
    # Configure the mock parser to return a populated execution graph
    plan = VisionTaskPlan(
        original_prompt="fake prompt",
        is_executable=True,
        missing_context=[],
        steps=[
            VisionStep(step_id=1, action_type=VisionActionType.FOCUS_WINDOW, target_element="Notepad", confidence=1.0),
            VisionStep(step_id=2, action_type=VisionActionType.CLICK_TEXT, target_element="File", confidence=1.0),
            VisionStep(step_id=3, action_type=VisionActionType.TYPE_TEXT, input_data="Hello World", confidence=1.0),
        ]
    )
    shell_with_mocks.parser.parse.return_value = plan
    
    # Run the shell: Execute action -> Check memory -> Exit
    with patch('builtins.input', side_effect=['execute fake plan', 'memory', 'exit']):
        # Patch sleep to make the test run instantaneously
        with patch('openoperator.agent.task_runner.time.sleep', return_value=None):
            shell_with_mocks.cmdloop()
            
    captured = capsys.readouterr().out
    
    assert "Current Session Memory" in captured
    assert "Last Window: Notepad" in captured
    assert "Last Click: File" in captured
    assert "Last Typed: Hello World" in captured