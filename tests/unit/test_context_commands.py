# D:\OpenOperator\tests\unit\test_context_commands.py

"""
Unit tests for Context-Aware Follow-Up Commands.

This suite defines the expected behavior for Issue #34, where the Intent Parser
must leverage the ActionMemoryManager to infer missing context (like targets or 
windows) from previous commands. 

Following Test-Driven Development (TDD), these tests are written before 
the implementation and are expected to fail initially.
"""

import pytest

from openoperator.agent.action_memory_manager import ActionMemoryManager
from openoperator.agent.intent_parser import VisionIntentParser
from openoperator.agent.vision_models import VisionActionType


@pytest.fixture
def empty_memory() -> ActionMemoryManager:
    """Provides a fresh ActionMemoryManager with no history."""
    return ActionMemoryManager()


@pytest.fixture
def populated_memory() -> ActionMemoryManager:
    """Provides an ActionMemoryManager with pre-existing session context."""
    memory = ActionMemoryManager()
    memory.remember_window("Notepad")
    memory.remember_click("File")
    return memory


@pytest.fixture
def parser_with_memory(populated_memory: ActionMemoryManager) -> VisionIntentParser:
    """
    Provides an IntentParser injected with populated memory.
    Note: The parser currently doesn't accept memory in its __init__, 
    so this test defines the expected future signature.
    """
    # EXPECTED FUTURE API: VisionIntentParser(memory=ActionMemoryManager)
    # This will fail until the parser is updated to accept memory.
    return VisionIntentParser(memory=populated_memory)


@pytest.fixture
def parser_without_memory() -> VisionIntentParser:
    """Provides a standard IntentParser for backward compatibility checks."""
    return VisionIntentParser()


def test_follow_up_type_command_uses_memory(parser_with_memory: VisionIntentParser) -> None:
    """
    Test that a command missing a focus window or click target infers 
    the context from memory.
    
    Prompt: "type hello world"
    Expected: Because "Notepad" is in memory as the last window, the parser 
    should prepend a FOCUS_WINDOW step to ensure context is maintained.
    """
    plan = parser_with_memory.parse("type hello world")
    
    assert plan.is_executable is True
    assert len(plan.steps) == 2
    
    # Inferred Context Step
    assert plan.steps[0].action_type == VisionActionType.FOCUS_WINDOW
    assert plan.steps[0].target_element == "Notepad"
    
    # Explicit Action Step
    assert plan.steps[1].action_type == VisionActionType.TYPE_TEXT
    assert plan.steps[1].input_data == "hello world"


def test_follow_up_click_command_uses_memory(parser_with_memory: VisionIntentParser) -> None:
    """
    Test that a standalone click command infers the target window from memory.
    
    Prompt: "click Edit"
    Expected: Injects a FOCUS_WINDOW step for "Notepad" before clicking "Edit".
    """
    plan = parser_with_memory.parse("click Edit")
    
    assert plan.is_executable is True
    assert len(plan.steps) == 2
    
    # Inferred Context Step
    assert plan.steps[0].action_type == VisionActionType.FOCUS_WINDOW
    assert plan.steps[0].target_element == "Notepad"
    
    # Explicit Action Step
    assert plan.steps[1].action_type == VisionActionType.CLICK_TEXT
    assert plan.steps[1].target_element == "Edit"


def test_empty_memory_ignores_follow_up(empty_memory: ActionMemoryManager) -> None:
    """
    Test that if memory is empty, the parser does not attempt to inject 
    missing context and purely parses the explicit intent. Validation of the 
    resulting plan's viability is the responsibility of downstream components.
    """
    # EXPECTED FUTURE API
    parser = VisionIntentParser(memory=empty_memory)
    
    plan = parser.parse("type hello world")
    
    # Verify that the parsed plan contains ONLY the explicit instruction,
    # with no inferred FOCUS_WINDOW step injected.
    assert len(plan.steps) == 1
    assert plan.steps[0].action_type == VisionActionType.TYPE_TEXT
    assert plan.steps[0].input_data == "hello world"


def test_backward_compatibility_explicit_commands(parser_with_memory: VisionIntentParser) -> None:
    """
    Test that explicitly provided context overrides memory context.
    
    Prompt: "switch to Chrome and click Search"
    Expected: "Chrome" overrides "Notepad" from memory.
    """
    plan = parser_with_memory.parse("switch to Chrome and click Search")
    
    assert plan.is_executable is True
    assert len(plan.steps) == 2
    
    assert plan.steps[0].action_type == VisionActionType.FOCUS_WINDOW
    assert plan.steps[0].target_element == "Chrome"
    assert plan.steps[0].target_element != "Notepad"
    
    assert plan.steps[1].action_type == VisionActionType.CLICK_TEXT
    assert plan.steps[1].target_element == "Search"


def test_backward_compatibility_no_memory_provided(parser_without_memory: VisionIntentParser) -> None:
    """
    Test that the parser functions exactly as before if no memory manager is injected.
    """
    plan = parser_without_memory.parse("open Calculator and type 5")
    
    assert plan.is_executable is True
    assert len(plan.steps) == 2
    
    assert plan.steps[0].action_type == VisionActionType.FOCUS_WINDOW
    assert plan.steps[0].target_element == "Calculator"
    
    assert plan.steps[1].action_type == VisionActionType.TYPE_TEXT
    assert plan.steps[1].input_data == "5"