from pathlib import Path

from openoperator.memory.storage import MemoryStorage


def test_save_and_load(tmp_path: Path):
    storage = MemoryStorage(
        str(tmp_path / "memory.json")
    )

    data = {
        "window": "Notepad",
        "click": "File",
    }

    assert storage.save(data) is True

    loaded = storage.load()

    assert loaded == data


def test_load_missing_file(tmp_path: Path):
    storage = MemoryStorage(
        str(tmp_path / "missing.json")
    )

    assert storage.load() == {}


def test_clear_storage(tmp_path: Path):
    storage = MemoryStorage(
        str(tmp_path / "memory.json")
    )

    storage.save(
        {"test": "value"}
    )

    assert storage.clear() is True
    assert storage.load() == {}


def test_corrupted_json_returns_empty_dict(
    tmp_path: Path,
):
    file_path = tmp_path / "memory.json"

    file_path.write_text(
        "{invalid json",
        encoding="utf-8",
    )

    storage = MemoryStorage(
        str(file_path)
    )

    assert storage.load() == {}