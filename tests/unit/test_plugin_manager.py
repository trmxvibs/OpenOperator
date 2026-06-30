"""
Tests for the OpenOperator Plugin Architecture.
"""

import pytest
from typing import Any, Dict
from openoperator.plugins.base import OpenOperatorPlugin
from openoperator.plugins.manager import PluginManager


class DummyWeatherPlugin(OpenOperatorPlugin):
    """A simple mock plugin for testing purposes."""
    
    @property
    def name(self) -> str:
        return "WeatherAPI"

    @property
    def version(self) -> str:
        return "1.0.0"

    def initialize(self, context: Dict[str, Any]) -> None:
        self.api_key = context.get("api_key", "default_key")

    def execute(self, command: str, **kwargs) -> Any:
        if command == "get_temp":
            city = kwargs.get("city", "Unknown")
            return f"Temperature in {city} is 25C using key {self.api_key}"
        raise ValueError(f"Unknown command: {command}")


@pytest.fixture
def manager():
    return PluginManager()


def test_register_plugin_success(manager):
    """Test that a valid plugin is registered correctly."""
    context = {"api_key": "test_123"}
    success = manager.register_plugin(DummyWeatherPlugin, context)
    
    assert success is True
    assert "weatherapi" in manager.list_plugins()


def test_execute_plugin_command_success(manager):
    """Test that commands are properly routed to the plugin execution method."""
    manager.register_plugin(DummyWeatherPlugin, {"api_key": "test_123"})
    
    result = manager.execute_plugin_command("WeatherAPI", "get_temp", city="London")
    assert result == "Temperature in London is 25C using key test_123"


def test_execute_plugin_command_not_found(manager):
    """Test executing a command on a plugin that does not exist."""
    result = manager.execute_plugin_command("NonExistentPlugin", "do_something")
    assert result is None


def test_execute_plugin_command_internal_error(manager):
    """Test handling of internal plugin errors."""
    manager.register_plugin(DummyWeatherPlugin)
    
    # Passing an unknown command raises a ValueError inside the plugin
    result = manager.execute_plugin_command("WeatherAPI", "crash_me")
    assert result is None