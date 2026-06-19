from openoperator.agent.action_memory_manager import (
    ActionMemoryManager,
)

from openoperator.memory.storage import (
    MemoryStorage,
)


def test_memory_can_be_saved_and_restored(
    tmp_path,
):
    storage = MemoryStorage(
        str(tmp_path / "memory.json")
    )

    manager = ActionMemoryManager()

    manager.remember_window(
        "Notepad"
    )

    manager.remember_click(
        "File"
    )

    manager.remember_type(
        "Hello"
    )

    assert storage.save(
        manager.export_state()
    ) is True

    restored = ActionMemoryManager()

    restored.import_state(
        storage.load()
    )

    assert restored.last_window == "Notepad"
    assert restored.last_click == "File"
    assert restored.last_typed == "Hello"

    assert len(
        restored.action_history
    ) == 3