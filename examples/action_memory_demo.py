"""
Demonstration of the ActionMemory system for OpenOperator.

This script populates an in-memory action log and exports the history
as a formatted JSON payload.
"""

import logging
from datetime import datetime, timezone

from pydantic import BaseModel

from openoperator.core.action_memory import ActionMemory, ActionRecord


class MemoryExport(BaseModel):
    """
    Wrapper model used to serialize the complete memory state into a single JSON payload.
    """
    total_records: int
    history: list[ActionRecord]


def main() -> None:
    """
    Main entry point for the Action Memory demonstration.
    """
    # Configure basic logging for the demo
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    logger.info("Initializing ActionMemory...")
    memory = ActionMemory()

    logger.info("Populating memory with mock action records...")

    # Record 1: Move Action
    memory.add_record(
        ActionRecord(
            step=1,
            action="move",
            status="success",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
    )

    # Record 2: Click Action
    memory.add_record(
        ActionRecord(
            step=2,
            action="click",
            status="success",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
    )

    # Record 3: Type Action
    memory.add_record(
        ActionRecord(
            step=3,
            action="type hello world",
            status="success",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
    )

    logger.info("Retrieving records from memory...")
    records = memory.get_records()

    # Wrap in a root model to dump the entire list cleanly as one JSON payload
    export_payload = MemoryExport(
        total_records=len(records),
        history=records
    )

    print("\n" + "=" * 50)
    print("ACTION MEMORY JSON EXPORT:")
    print("=" * 50)
    print(export_payload.model_dump_json(indent=4))
    print("=" * 50 + "\n")

    logger.info("Memory demo complete.")


if __name__ == "__main__":
    main()