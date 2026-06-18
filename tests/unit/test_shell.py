"""
Unit tests for the InteractiveShell.

Ensures that the shell gracefully handles user inputs, correctly interacts
with the intent parser and task runner, and does not crash on unexpected exceptions.
"""

from unittest.mock import MagicMock, patch

import pytest

from openoperator.agent.vision_models import VisionTaskPlan
from openoperator.shell import InteractiveShell


@pytest.fixture
def mocks() -> dict[str, MagicMock]:
    """Provides pre-configured mock subsystems."""
    return {
        "parser": MagicMock(),
        "runner": MagicMock()
    }


@pytest.fixture
def shell(mocks: dict[str, MagicMock]) -> InteractiveShell:
    """Provides an InteractiveShell injected with mocks."""
    return InteractiveShell(parser=mocks["parser"], runner=mocks["runner"])


@patch("builtins.input", side_effect=["exit"])
def test_shell_exit_command(mock_input: MagicMock, shell: InteractiveShell, mocks: dict[str, MagicMock]) -> None:
    """Test that typing 'exit' breaks the loop cleanly."""
    shell.cmdloop()
    mocks["parser"].parse.assert_not_called()


@patch("builtins.input", side_effect=["quit"])
def test_shell_quit_command(mock_input: MagicMock, shell: InteractiveShell, mocks: dict[str, MagicMock]) -> None:
    """Test that typing 'quit' breaks the loop cleanly."""
    shell.cmdloop()
    mocks["parser"].parse.assert_not_called()


@patch("builtins.input", side_effect=EOFError)
def test_shell_eof_handling(mock_input: MagicMock, shell: InteractiveShell, mocks: dict[str, MagicMock]) -> None:
    """Test that CTRL+D (EOFError) gracefully exits without crashing."""
    shell.cmdloop()
    mocks["parser"].parse.assert_not_called()


@patch("builtins.input", side_effect=KeyboardInterrupt)
def test_shell_keyboard_interrupt_handling(mock_input: MagicMock, shell: InteractiveShell, mocks: dict[str, MagicMock]) -> None:
    """Test that CTRL+C (KeyboardInterrupt) gracefully exits without crashing."""
    shell.cmdloop()
    mocks["parser"].parse.assert_not_called()


@patch("builtins.input", side_effect=["open notepad", "exit"])
def test_shell_valid_command_execution(mock_input: MagicMock, shell: InteractiveShell, mocks: dict[str, MagicMock]) -> None:
    """Test that a valid natural language command is parsed and executed."""
    mock_plan = MagicMock(spec=VisionTaskPlan)
    mock_plan.is_executable = True
    mock_plan.steps = [1]
    
    mocks["parser"].parse.return_value = mock_plan
    mocks["runner"].execute_plan.return_value = True
    
    shell.cmdloop()
    
    mocks["parser"].parse.assert_called_once_with("open notepad")
    mocks["runner"].execute_plan.assert_called_once_with(mock_plan, delay_between_steps=1.0)


@patch("builtins.input", side_effect=["open", "exit"])
def test_shell_non_executable_command(mock_input: MagicMock, shell: InteractiveShell, mocks: dict[str, MagicMock]) -> None:
    """Test that missing context prevents execution from triggering."""
    mock_plan = MagicMock(spec=VisionTaskPlan)
    mock_plan.is_executable = False
    mock_plan.missing_context = ["Missing target window"]
    
    mocks["parser"].parse.return_value = mock_plan
    
    shell.cmdloop()
    
    mocks["parser"].parse.assert_called_once_with("open")
    mocks["runner"].execute_plan.assert_not_called()


@patch("builtins.input", side_effect=["trigger error", "exit"])
def test_shell_exception_handling(mock_input: MagicMock, shell: InteractiveShell, mocks: dict[str, MagicMock]) -> None:
    """Test that an internal exception during parsing/execution does not crash the loop."""
    mocks["parser"].parse.side_effect = Exception("Simulated severe crash")
    
    # The shell should catch the error, print it, and loop to the "exit" command.
    # If it crashes, this test will fail.
    shell.cmdloop()