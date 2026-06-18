"""
Interactive shell module for OpenOperator.

Provides a persistent command-line interface that allows users to continuously
input natural language instructions. It parses intents and delegates execution
to the TaskRunner while gracefully handling exceptions.
"""

import logging
import sys
from typing import Optional

# Importing readline automatically enables command history for the built-in input() function.
# This works natively on Unix/Mac. On Windows, it requires 'pyreadline3', but we 
# gracefully degrade if it's not installed.
try:
    import readline
except ImportError:
    pass

from openoperator.agent.intent_parser import VisionIntentParser
from openoperator.agent.task_runner import TaskRunner

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
        """
        Initializes the InteractiveShell with NLP and Execution subsystems.
        """
        self.parser = parser or VisionIntentParser()
        self.runner = runner or TaskRunner()

    def cmdloop(self) -> None:
        """
        Starts the persistent read-eval-print loop (REPL).
        """
        print("\n" + "=" * 60)
        print(" Welcome to the OpenOperator Interactive Shell ")
        print("=" * 60)
        print("Type natural language commands to control the agent.")
        print("Examples:")
        print("  - switch to Notepad")
        print("  - click File and type Hello World")
        print("  - type OpenOperator")
        print("Type 'exit' or 'quit' to close the shell.")
        print("-" * 60 + "\n")

        while True:
            try:
                # The persistent prompt requested for the shell
                user_input = input("OpenOperator > ").strip()
            except (EOFError, KeyboardInterrupt):
                # Handle CTRL+C and CTRL+D gracefully without stack traces
                print("\nExiting shell. Goodbye!")
                break

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            self.handle_command(user_input)

    def handle_command(self, user_input: str) -> None:
        """
        Parses and executes a single natural language command.
        Contains exception handling to prevent the shell from crashing on bad input.

        Args:
            user_input (str): The raw string input from the user.
        """
        try:
            logger.debug(f"Shell received command: '{user_input}'")
            
            # Parse natural language into a structured execution graph
            plan = self.parser.parse(user_input)
            
            if not plan.is_executable:
                print("[!] Cannot execute plan. Missing context:")
                for context in plan.missing_context:
                    print(f"    - {context}")
                return

            print(f"[*] Executing plan with {len(plan.steps)} steps...")
            
            # Execute the compiled graph dynamically
            success = self.runner.execute_plan(plan, delay_between_steps=1.0)
            
            if success:
                print("[+] Sequence completed successfully.\n")
            else:
                print("[-] Sequence failed or was aborted.\n")
                
        except Exception as e:
            logger.error(f"Unexpected error in shell execution: {e}", exc_info=True)
            print(f"[!] An unexpected internal error occurred: {e}\n")