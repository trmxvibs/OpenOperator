"""
Standalone demonstration of the OpenOperator Interactive Shell.
"""

import logging
import sys

from openoperator.shell import InteractiveShell


def main() -> None:
    """
    Initializes and starts the interactive REPL shell demonstration.
    """
    # Set to WARNING so execution debug logs don't clutter the interactive experience
    logging.basicConfig(level=logging.WARNING)

    if sys.platform != "win32":
        print("Warning: Window Focus commands are currently only supported on Windows.")

    shell = InteractiveShell()
    shell.cmdloop()


if __name__ == "__main__":
    main()