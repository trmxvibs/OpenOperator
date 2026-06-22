# D:\OpenOperator\tests\integration\conftest.py

"""
Pytest configuration and shared fixtures for OpenOperator integration tests.

This module ensures that integration tests are strictly executed in a native 
Windows environment, skipping them gracefully on unsupported platforms. It also 
provides robust shared fixtures for environment management and process cleanup.
"""

import subprocess
import sys
from typing import Generator, List

import pytest


def pytest_runtest_setup(item: pytest.Item) -> None:
    """
    Hook to dynamically evaluate test execution requirements.
    Automatically skips any test in the 'integration' directory if the 
    underlying operating system is not Windows.
    
    Args:
        item (pytest.Item): The current test item being evaluated.
    """
    # Assuming this conftest.py is specifically within the /integration/ directory,
    # it applies to all tests residing alongside or beneath it.
    if sys.platform != "win32":
        pytest.skip(f"Skipping {item.name}: OpenOperator integration tests require Windows ('win32').")


@pytest.fixture
def managed_process() -> Generator[List[subprocess.Popen], None, None]:
    """
    A robust cleanup fixture that tracks and terminates spawned Windows processes.
    
    Integration tests can append `subprocess.Popen` objects to the yielded list. 
    Regardless of test outcome (pass/fail/error), this fixture guarantees that 
    all registered processes are forcefully terminated during teardown.
    
    Yields:
        List[subprocess.Popen]: A list to populate with active processes.
    """
    processes: List[subprocess.Popen] = []
    
    yield processes
    
    # Teardown phase: forcefully clean up all tracked processes
    for process in processes:
        if process.poll() is None:  # Process is still running
            try:
                process.terminate()
                # Allow a brief grace period for graceful shutdown
                process.wait(timeout=3.0)
            except subprocess.TimeoutExpired:
                # Force kill if the process hangs
                process.kill()
            except Exception as e:
                # Catch access denied or invalid handles if the process already died
                print(f"Warning: Failed to cleanly terminate process {process.pid}: {e}")