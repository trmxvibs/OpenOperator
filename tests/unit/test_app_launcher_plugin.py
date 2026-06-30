"""
Tests for the AppLauncherPlugin.
Ensures applications can be safely launched via subprocess mocking.
"""

import pytest
from unittest.mock import patch, MagicMock
from openoperator.plugins.app_launcher import AppLauncherPlugin


@pytest.fixture
def launcher():
    plugin = AppLauncherPlugin()
    plugin.initialize({})
    return plugin


def test_plugin_metadata(launcher):
    """Verify plugin properties match the base architecture requirements."""
    assert launcher.name == "AppLauncher"
    assert launcher.version == "1.0.0"


def test_execute_launch_success(launcher):
    """Test successful application launch command."""
    with patch("subprocess.Popen") as mock_popen:
        result = launcher.execute("launch", app_name="notepad")
        
        assert result is True
        mock_popen.assert_called_once_with("notepad", shell=True)


def test_execute_invalid_command(launcher):
    """Test that unsupported commands return False gracefully."""
    result = launcher.execute("destroy", app_name="notepad")
    assert result is False


def test_execute_missing_app_name(launcher):
    """Test that missing required arguments are handled properly."""
    result = launcher.execute("launch")  # Missing app_name
    assert result is False


def test_execute_subprocess_exception(launcher):
    """Test that OS-level errors during launch do not crash the framework."""
    with patch("subprocess.Popen", side_effect=FileNotFoundError("Executable not found")):
        result = launcher.execute("launch", app_name="invalid_app_123")
        assert result is False