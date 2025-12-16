"""
Tests for the Plugins Module.
"""

import pytest

from chatbot.plugins import Plugin, PluginInfo, PluginManager, get_plugin_manager


class MockPlugin(Plugin):
    """Mock plugin for testing."""

    def __init__(self, name: str = "mock"):
        self._name = name
        self.loaded = False
        self.unloaded = False

    @property
    def info(self) -> PluginInfo:
        return PluginInfo(
            name=self._name,
            version="1.0.0",
            description="A mock plugin",
        )

    def on_load(self):
        self.loaded = True

    def on_unload(self):
        self.unloaded = True

    def on_message(self, message: str):
        return message.upper()

    def on_response(self, response: str):
        return response + "!"


class TestPluginInfo:
    """Test PluginInfo dataclass."""

    def test_creation(self):
        info = PluginInfo(
            name="test",
            version="1.0.0",
            description="Test plugin",
        )
        assert info.name == "test"
        assert info.version == "1.0.0"

    def test_optional_author(self):
        info = PluginInfo(
            name="test",
            version="1.0.0",
            description="Test",
            author="Author",
        )
        assert info.author == "Author"


class TestPluginManager:
    """Test PluginManager class."""

    def test_initialization(self):
        manager = PluginManager()
        assert manager is not None

    def test_register(self):
        manager = PluginManager()
        plugin = MockPlugin()
        manager.register(plugin)
        assert manager.get("mock") is not None

    def test_unregister(self):
        manager = PluginManager()
        plugin = MockPlugin()
        manager.register(plugin)
        result = manager.unregister("mock")
        assert result is True
        assert manager.get("mock") is None

    def test_enable(self):
        manager = PluginManager()
        plugin = MockPlugin()
        manager.register(plugin)
        manager.enable("mock")
        assert plugin.loaded is True
        assert "mock" in manager.list_enabled()

    def test_disable(self):
        manager = PluginManager()
        plugin = MockPlugin()
        manager.register(plugin)
        manager.enable("mock")
        manager.disable("mock")
        assert plugin.unloaded is True
        assert "mock" not in manager.list_enabled()

    def test_list_all(self):
        manager = PluginManager()
        manager.register(MockPlugin("plugin1"))
        manager.register(MockPlugin("plugin2"))
        plugins = manager.list_all()
        assert len(plugins) == 2

    def test_process_message(self):
        manager = PluginManager()
        plugin = MockPlugin()
        manager.register(plugin)
        manager.enable("mock")
        result = manager.process_message("hello")
        assert result == "HELLO"

    def test_process_response(self):
        manager = PluginManager()
        plugin = MockPlugin()
        manager.register(plugin)
        manager.enable("mock")
        result = manager.process_response("hello")
        assert result == "hello!"


class TestGetPluginManager:
    """Test get_plugin_manager function."""

    def test_returns_manager(self):
        manager = get_plugin_manager()
        assert isinstance(manager, PluginManager)
