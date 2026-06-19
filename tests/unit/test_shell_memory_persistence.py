from pathlib import Path

from openoperator.agent.action_memory_manager import (
    ActionMemoryManager,
)

from openoperator.memory.storage import (
    MemoryStorage,
)


def test_memory_persistence_round_trip(
    tmp_path: Path,
):

    storage = MemoryStorage(
        str(
            tmp_path / "memory.json"
        )
    )

    memory = ActionMemoryManager()

    memory.remember_window(
        "Chrome"
    )

    memory.remember_click(
        "Search"
    )

    memory.remember_type(
        "OpenOperator"
    )

    assert storage.save(
        memory.export_state()
    ) is True

    restored = ActionMemoryManager()

    restored.import_state(
        storage.load()
    )

    assert restored.last_window == "Chrome"

    assert restored.last_click == "Search"

    assert restored.last_typed == "OpenOperator"

    assert len(
        restored.action_history
    ) == 3