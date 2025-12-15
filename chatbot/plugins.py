"""
Plugin System Module

Provides a base plugin architecture for extensibility.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Type
from dataclasses import dataclass


@dataclass
class PluginInfo:
    """Plugin metadata."""

    name: str
    version: str
    description: str
    author: Optional[str] = None


class Plugin(ABC):
    """Base class for plugins."""

    @property
    @abstractmethod
    def info(self) -> PluginInfo:
        """Get plugin information."""
        pass

    def on_load(self) -> None:
        """Called when plugin is loaded."""
        pass

    def on_unload(self) -> None:
        """Called when plugin is unloaded."""
        pass

    def on_message(self, message: str) -> Optional[str]:
        """Process an incoming message."""
        return None

    def on_response(self, response: str) -> str:
        """Process an outgoing response."""
        return response

    def on_sentiment(self, score: float, label: str) -> None:
        """Called when sentiment is analyzed."""
        pass


class PluginManager:
    """Manages plugin lifecycle."""

    def __init__(self):
        """Initialize plugin manager."""
        self._plugins: Dict[str, Plugin] = {}
        self._enabled: Dict[str, bool] = {}

    def register(self, plugin: Plugin) -> None:
        """Register a plugin."""
        name = plugin.info.name
        self._plugins[name] = plugin
        self._enabled[name] = False

    def unregister(self, name: str) -> bool:
        """Unregister a plugin."""
        if name in self._plugins:
            if self._enabled.get(name):
                self.disable(name)
            del self._plugins[name]
            del self._enabled[name]
            return True
        return False

    def enable(self, name: str) -> bool:
        """Enable a plugin."""
        if name in self._plugins and not self._enabled.get(name):
            self._plugins[name].on_load()
            self._enabled[name] = True
            return True
        return False

    def disable(self, name: str) -> bool:
        """Disable a plugin."""
        if name in self._plugins and self._enabled.get(name):
            self._plugins[name].on_unload()
            self._enabled[name] = False
            return True
        return False

    def get(self, name: str) -> Optional[Plugin]:
        """Get a plugin by name."""
        return self._plugins.get(name)

    def list_all(self) -> List[PluginInfo]:
        """List all registered plugins."""
        return [p.info for p in self._plugins.values()]

    def list_enabled(self) -> List[str]:
        """List enabled plugins."""
        return [name for name, enabled in self._enabled.items() if enabled]

    def process_message(self, message: str) -> str:
        """Run message through enabled plugins."""
        result = message
        for name in self.list_enabled():
            plugin = self._plugins[name]
            processed = plugin.on_message(result)
            if processed is not None:
                result = processed
        return result

    def process_response(self, response: str) -> str:
        """Run response through enabled plugins."""
        result = response
        for name in self.list_enabled():
            plugin = self._plugins[name]
            result = plugin.on_response(result)
        return result


# Global plugin manager
_manager = PluginManager()


def get_plugin_manager() -> PluginManager:
    """Get the global plugin manager."""
    return _manager
