"""
Unit tests for the ActionMemory system.
"""

import pytest

from openoperator.core.action_memory import ActionMemory, ActionRecord


@pytest.fixture
def memory() -> ActionMemory:
    """Fixture providing a fresh ActionMemory instance for each test."""
    return ActionMemory()


def test_add_single_record(memory: ActionMemory) -> None:
    """Test that a single record can be added and retrieved correctly."""
    record = ActionRecord(
        step=1,
        action="move",
        status="success",
        timestamp="2023-10-01T12:00:00Z"
    )
    
    memory.add_record(record)
    records = memory.get_records()
    
    assert len(records) == 1
    assert records[0].step == 1
    assert records[0].action == "move"
    assert records[0].status == "success"
    assert records[0].timestamp == "2023-10-01T12:00:00Z"


def test_add_multiple_records_preserves_order(memory: ActionMemory) -> None:
    """Test that multiple records are stored and retrieved in their insertion order."""
    record1 = ActionRecord(step=1, action="move", status="success", timestamp="T1")
    record2 = ActionRecord(step=2, action="click", status="success", timestamp="T2")
    record3 = ActionRecord(step=3, action="type hello", status="failed", timestamp="T3")

    memory.add_record(record1)
    memory.add_record(record2)
    memory.add_record(record3)

    records = memory.get_records()
    
    assert len(records) == 3
    assert records[0].step == 1
    assert records[0].action == "move"
    assert records[1].step == 2
    assert records[1].action == "click"
    assert records[2].step == 3
    assert records[2].action == "type hello"


def test_clear_memory(memory: ActionMemory) -> None:
    """Test that clearing the memory completely removes all stored records."""
    record1 = ActionRecord(step=1, action="move", status="success", timestamp="T1")
    record2 = ActionRecord(step=2, action="click", status="success", timestamp="T2")
    
    memory.add_record(record1)
    memory.add_record(record2)
    
    assert len(memory.get_records()) == 2
    
    memory.clear()
    
    assert len(memory.get_records()) == 0


def test_get_records_returns_copy(memory: ActionMemory) -> None:
    """Test that get_records() returns a shallow copy to prevent external mutation."""
    record1 = ActionRecord(step=1, action="move", status="success", timestamp="T1")
    memory.add_record(record1)

    # Retrieve the list of records and attempt to mutate it
    external_list = memory.get_records()
    assert len(external_list) == 1
    
    record2 = ActionRecord(step=2, action="click", status="success", timestamp="T2")
    external_list.append(record2)
    
    # Verify the internal list remains unaffected
    internal_list = memory.get_records()
    assert len(internal_list) == 1
    assert internal_list[0].step == 1
    assert "click" not in [r.action for r in internal_list]