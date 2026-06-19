"""
Interactive shell module for OpenOperator.

Provides a persistent command-line interface that allows users to continuously
input natural language instructions. It parses intents and delegates execution
to the TaskRunner while gracefully handling exceptions.
"""

import logging
from typing import Optional

try:
    import readline
except ImportError:
    pass

from openoperator.agent.intent_parser import VisionIntentParser
from openoperator.agent.task_runner import TaskRunner
from openoperator.memory.storage import MemoryStorage

logger = logging.getLogger(__name__)


class InteractiveShell:
    """
    A persistent interactive shell for OpenOperator.
    Accepts natural language input, handles parsing, and orchestrates task execution.
    """

    def __init__(
        self,
        parser: Optional[VisionIntentParser] = None,
        runner: Optional[TaskRunner] = None
    ) -> None:

        self.parser = parser or VisionIntentParser()
        self.runner = runner or TaskRunner()

        self.storage = MemoryStorage()

        loaded_state = self.storage.load()

        if loaded_state:
            self.runner.memory.import_state(
                loaded_state
            )

    def save_memory(self) -> None:
        """
        Persist current memory state.
        """

        self.storage.save(
            self.runner.memory.export_state()
        )

    def cmdloop(self) -> None:

        print("\n" + "=" * 60)
        print(" Welcome to the OpenOperator Interactive Shell ")
        print("=" * 60)
        print("Type natural language commands to control the agent.")
        print("Examples:")
        print("  - switch to Notepad")
        print("  - click File and type Hello World")
        print("  - memory (Displays current session memory)")
        print("Type 'exit' or 'quit' to close the shell.")
        print("-" * 60 + "\n")

        while True:

            try:
                user_input = input(
                    "OpenOperator > "
                ).strip()

            except (EOFError, KeyboardInterrupt):

                self.save_memory()

                print(
                    "\nExiting shell. Goodbye!"
                )

                break

            if not user_input:
                continue

            if user_input.lower() in (
                "exit",
                "quit",
            ):

                self.save_memory()

                print("Goodbye!")

                break

            if user_input.lower() == "memory":
                self.display_memory()
                continue

            self.handle_command(
                user_input
            )

    def display_memory(self) -> None:

        mem = self.runner.memory.get_memory()

        print("\nCurrent Session Memory")
        print(
            f"Last Window: {mem.get('last_window') or 'None'}"
        )
        print(
            f"Last Click: {mem.get('last_click') or 'None'}"
        )
        print(
            f"Last Typed: {mem.get('last_typed') or 'None'}"
        )
        print()

    def handle_command(
        self,
        user_input: str,
    ) -> None:

        try:

            logger.debug(
                f"Shell received command: '{user_input}'"
            )

            plan = self.parser.parse(
                user_input
            )

            if not plan.is_executable:

                print(
                    "[!] Cannot execute plan. Missing context:"
                )

                for context in plan.missing_context:
                    print(
                        f"    - {context}"
                    )

                return

            print(
                f"[*] Executing plan with {len(plan.steps)} steps..."
            )

            success = self.runner.execute_plan(
                plan,
                delay_between_steps=1.0,
            )

            if success:
                print(
                    "[+] Sequence completed successfully.\n"
                )
            else:
                print(
                    "[-] Sequence failed or was aborted.\n"
                )

        except Exception as e:

            logger.error(
                f"Unexpected error in shell execution: {e}",
                exc_info=True,
            )

            print(
                f"[!] An unexpected internal error occurred: {e}\n"
            )