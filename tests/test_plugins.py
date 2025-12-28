"""Tests for plugins module."""

import pytest
from chatbot.plugins import (
    PluginType,
    PluginPriority,
    PluginInfo,
    Plugin,
    PluginManager,
    create_simple_plugin,
)


class MockPlugin(Plugin):
    """Mock plugin for testing."""

    def __init__(self, name: str = "mock"):
        self._name = name
        self._initialized = False

    @property
    def info(self) -> PluginInfo:
        return PluginInfo(
            name=self._name,
            version="1.0.0",
            description="Mock plugin",
        )

    def initialize(self, config):
        self._initialized = True

    def execute(self, data):
        return f"processed:{data}"


class TestPluginManager:
    """Tests for PluginManager."""

    def test_register_plugin(self):
        """Test registering plugin."""
        manager = PluginManager()
        plugin = MockPlugin("test")
        manager.register(plugin)
        
        assert manager.get_plugin("test") is not None

    def test_unregister_plugin(self):
        """Test unregistering plugin."""
        manager = PluginManager()
        plugin = MockPlugin("test")
        manager.register(plugin)
        
        result = manager.unregister("test")
        assert result is True
        assert manager.get_plugin("test") is None

    def test_initialize_all(self):
        """Test initializing all plugins."""
        manager = PluginManager()
        plugin = MockPlugin("test")
        manager.register(plugin)
        manager.initialize_all()
        
        assert plugin._initialized is True

    def test_get_plugins_by_type(self):
        """Test getting plugins by type."""
        manager = PluginManager()
        plugin = MockPlugin("test")
        manager.register(plugin)
        
        plugins = manager.get_plugins_by_type(PluginType.ANALYZER)
        assert len(plugins) == 1

    def test_list_plugins(self):
        """Test listing plugins."""
        manager = PluginManager()
        manager.register(MockPlugin("a"))
        manager.register(MockPlugin("b"))
        
        plugins = manager.list_plugins()
        assert len(plugins) == 2


class TestCreateSimplePlugin:
    """Tests for create_simple_plugin."""

    def test_create_plugin(self):
        """Test creating simple plugin."""
        plugin = create_simple_plugin(
            "upper",
            lambda x: x.upper(),
        )
        assert plugin.info.name == "upper"

    def test_execute_plugin(self):
        """Test executing simple plugin."""
        plugin = create_simple_plugin(
            "upper",
            lambda x: x.upper(),
        )
        result = plugin.execute("hello")
        assert result == "HELLO"
