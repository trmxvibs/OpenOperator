"""
Persistent storage for ActionMemoryManager.

Stores memory state as JSON on disk and restores it on startup.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class MemoryStorage:
    """
    Handles saving and loading memory state.
    """

    def __init__(self, storage_path: str = "outputs/memory.json") -> None:
        self.storage_path = Path(storage_path)

    def save(self, data: dict[str, Any]) -> bool:
        """
        Save memory data to disk.
        """
        try:
            self.storage_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with open(
                self.storage_path,
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(
                    data,
                    f,
                    indent=4,
                )

            return True

        except Exception:
            return False

    def load(self) -> dict[str, Any]:
        """
        Load memory data from disk.
        """

        if not self.storage_path.exists():
            return {}

        try:
            with open(
                self.storage_path,
                "r",
                encoding="utf-8",
            ) as f:
                return json.load(f)

        except Exception:
            return {}

    def clear(self) -> bool:
        """
        Delete stored memory file.
        """

        try:
            if self.storage_path.exists():
                self.storage_path.unlink()

            return True

        except Exception:
            return False