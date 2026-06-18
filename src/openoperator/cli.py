"""
Command Line Interface for OpenOperator.

This module provides the entry point for the `openoperator` command,
routing user commands to the appropriate demonstration functions or the interactive shell.
"""

import argparse
import logging
import sys

from openoperator.demos import (
    run_click_type_demo,
    run_mouse_demo,
    run_screenshot_demo,
    run_typing_demo,
)
from openoperator.perception.ocr import OCREngine
from openoperator.perception.screenshot import ScreenshotEngine
from openoperator.shell import InteractiveShell


def run_ocr_demo() -> None:
    """Demonstrates capturing the screen and extracting text via OCR."""
    logger = logging.getLogger(__name__)
    logger.info("--- Running OCR Demo ---")
    
    screenshot_engine = ScreenshotEngine()
    ocr_engine = OCREngine()
    
    logger.info("Capturing screen...")
    image_bytes = screenshot_engine.capture_screen()
    
    if not image_bytes:
        logger.error("Failed to capture screen.")
        return

    logger.info("Running OCR extraction...")
    text = ocr_engine.extract_text(image_bytes)
    
    print("\n" + "="*40)
    print("EXTRACTED TEXT:")
    print("="*40)
    print(text)
    print("="*40 + "\n")
    
    logger.info("OCR Demo complete.\n")


def run_interactive_shell() -> None:
    """Starts the persistent interactive natural language shell."""
    shell = InteractiveShell()
    shell.cmdloop()


def configure_logging() -> None:
    """Configures the standard logging format for CLI outputs."""
    # Set to WARNING to prevent verbose logs from cluttering the interactive prompt
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def create_parser() -> argparse.ArgumentParser:
    """
    Constructs the argument parser and defines all CLI commands.

    Returns:
        argparse.ArgumentParser: The configured parser instance.
    """
    parser = argparse.ArgumentParser(
        prog="openoperator",
        description="OpenOperator Command Line Interface for testing and demonstrations.",
    )

    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        required=True,
        help="Available commands",
    )

    screenshot_parser = subparsers.add_parser(
        "screenshot",
        help="Executes the screenshot capture demonstration.",
    )
    screenshot_parser.set_defaults(func=run_screenshot_demo)

    mouse_parser = subparsers.add_parser(
        "mouse-demo",
        help="Executes the mouse control demonstration.",
    )
    mouse_parser.set_defaults(func=run_mouse_demo)

    typing_parser = subparsers.add_parser(
        "typing-demo",
        help="Executes the keyboard typing demonstration.",
    )
    typing_parser.set_defaults(func=run_typing_demo)

    click_type_parser = subparsers.add_parser(
        "click-type-demo",
        help="Executes the combined mouse click and keyboard typing demonstration.",
    )
    click_type_parser.set_defaults(func=run_click_type_demo)

    ocr_parser = subparsers.add_parser(
        "ocr-demo",
        help="Executes the screen capture and OCR extraction demonstration.",
    )
    ocr_parser.set_defaults(func=run_ocr_demo)

    shell_parser = subparsers.add_parser(
        "shell",
        help="Starts the persistent interactive natural language shell.",
    )
    shell_parser.set_defaults(func=run_interactive_shell)

    return parser


def main() -> int:
    """
    Main execution entry point.

    Returns:
        int: Exit status code (0 for success, 1 for failure).
    """
    configure_logging()
    logger = logging.getLogger(__name__)
    
    parser = create_parser()
    args = parser.parse_args()

    try:
        # We don't log "Executing command" for the shell as it has its own UI
        if args.command != "shell":
            logger.setLevel(logging.INFO)
            logger.info(f"Executing command: {args.command}")
            
        args.func()
        
        if args.command != "shell":
            logger.info(f"Command '{args.command}' completed successfully.")
            
        return 0
    except KeyboardInterrupt:
        print("\nExecution interrupted by user.")
        return 0
    except Exception as e:
        logger.error(f"Execution failed during '{args.command}': {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())