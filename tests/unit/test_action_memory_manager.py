"""
Unit tests for the ActionMemoryManager.

Ensures that the agent correctly stores and retrieves session state, 
updates action history, and clears memory upon request.
"""

import pytest

from openoperator.agent.action_memory_manager import ActionMemoryManager


@pytest.fixture
def memory_manager() -> ActionMemoryManager:
    """Provides a fresh ActionMemoryManager instance for each test."""
    return ActionMemoryManager()


def test_initial_state(memory_manager: ActionMemoryManager) -> None:
    """Test that the memory manager initializes with empty fields."""
    mem = memory_manager.get_memory()
    assert mem["last_window"] is None
    assert mem["last_click"] is None
    assert mem["last_typed"] is None
    assert len(mem["action_history"]) == 0


def test_remember_window(memory_manager: ActionMemoryManager) -> None:
    """Test storing the last focused window."""
    memory_manager.remember_window("Notepad")
    mem = memory_manager.get_memory()
    
    assert mem["last_window"] == "Notepad"
    assert len(mem["action_history"]) == 1
    assert "Notepad" in mem["action_history"][0]


def test_remember_click(memory_manager: ActionMemoryManager) -> None:
    """Test storing the last clicked target."""
    memory_manager.remember_click("File")
    mem = memory_manager.get_memory()
    
    assert mem["last_click"] == "File"
    assert len(mem["action_history"]) == 1
    assert "File" in mem["action_history"][0]


def test_remember_type(memory_manager: ActionMemoryManager) -> None:
    """Test storing the last typed text."""
    memory_manager.remember_type("Hello World")
    mem = memory_manager.get_memory()
    
    assert mem["last_typed"] == "Hello World"
    assert len(mem["action_history"]) == 1
    assert "Hello World" in mem["action_history"][0]


def test_history_updates(memory_manager: ActionMemoryManager) -> None:
    """Test that multiple actions stack sequentially in the history."""
    memory_manager.remember_window("Chrome")
    memory_manager.remember_click("Search")
    memory_manager.remember_type("OpenOperator")
    
    mem = memory_manager.get_memory()
    
    assert mem["last_window"] == "Chrome"
    assert mem["last_click"] == "Search"
    assert mem["last_typed"] == "OpenOperator"
    assert len(mem["action_history"]) == 3
    assert mem["action_history"][0] == "Focused window: Chrome"
    assert mem["action_history"][1] == "Clicked text: Search"
    assert mem["action_history"][2] == "Typed text: OpenOperator"


def test_clear_memory(memory_manager: ActionMemoryManager) -> None:
    """Test that clearing memory resets all fields and history."""
    memory_manager.remember_window("Notepad")
    memory_manager.remember_click("File")
    
    assert len(memory_manager.get_memory()["action_history"]) == 2
    
    memory_manager.clear()
    mem = memory_manager.get_memory()
    
    assert mem["last_window"] is None
    assert mem["last_click"] is None
    assert mem["last_typed"] is None
    assert len(mem["action_history"]) == 0