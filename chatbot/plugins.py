"""
Plugin System Module

Extensible plugin architecture for sentiment analysis.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Type, Callable
from enum import Enum


class PluginType(Enum):
    """Plugin types."""

    PREPROCESSOR = "preprocessor"
    ANALYZER = "analyzer"
    POSTPROCESSOR = "postprocessor"
    FORMATTER = "formatter"
    VALIDATOR = "validator"


class PluginPriority(Enum):
    """Plugin execution priority."""

    FIRST = 0
    HIGH = 25
    NORMAL = 50
    LOW = 75
    LAST = 100


@dataclass
class PluginInfo:
    """Plugin metadata."""

    name: str
    version: str
    description: str
    author: str = ""
    plugin_type: PluginType = PluginType.ANALYZER
    priority: PluginPriority = PluginPriority.NORMAL
    dependencies: List[str] = field(default_factory=list)


class Plugin(ABC):
    """Base plugin class."""

    @property
    @abstractmethod
    def info(self) -> PluginInfo:
        """Get plugin info."""
        pass

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize plugin."""
        pass

    @abstractmethod
    def execute(self, data: Any) -> Any:
        """Execute plugin."""
        pass

    def cleanup(self) -> None:
        """Cleanup plugin resources."""
        pass


class PreprocessorPlugin(Plugin):
    """Plugin for text preprocessing."""

    @abstractmethod
    def preprocess(self, text: str) -> str:
        """Preprocess text."""
        pass

    def execute(self, data: Any) -> Any:
        if isinstance(data, str):
            return self.preprocess(data)
        return data


class AnalyzerPlugin(Plugin):
    """Plugin for sentiment analysis."""

    @abstractmethod
    def analyze(self, text: str) -> Dict[str, Any]:
        """Analyze text."""
        pass

    def execute(self, data: Any) -> Any:
        if isinstance(data, str):
            return self.analyze(data)
        return data


class PostprocessorPlugin(Plugin):
    """Plugin for result postprocessing."""

    @abstractmethod
    def postprocess(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Postprocess result."""
        pass

    def execute(self, data: Any) -> Any:
        if isinstance(data, dict):
            return self.postprocess(data)
        return data


class PluginManager:
    """Manage and execute plugins."""

    def __init__(self):
        """Initialize manager."""
        self._plugins: Dict[str, Plugin] = {}
        self._configs: Dict[str, Dict[str, Any]] = {}
        self._initialized: set = set()

    def register(
        self,
        plugin: Plugin,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Register a plugin."""
        name = plugin.info.name
        self._plugins[name] = plugin
        self._configs[name] = config or {}

    def unregister(self, name: str) -> bool:
        """Unregister a plugin."""
        if name in self._plugins:
            plugin = self._plugins[name]
            plugin.cleanup()
            del self._plugins[name]
            self._configs.pop(name, None)
            self._initialized.discard(name)
            return True
        return False

    def initialize_all(self) -> None:
        """Initialize all plugins."""
        for name, plugin in self._plugins.items():
            if name not in self._initialized:
                plugin.initialize(self._configs.get(name, {}))
                self._initialized.add(name)

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get plugin by name."""
        return self._plugins.get(name)

    def get_plugins_by_type(self, plugin_type: PluginType) -> List[Plugin]:
        """Get plugins by type."""
        plugins = [p for p in self._plugins.values() if p.info.plugin_type == plugin_type]
        return sorted(plugins, key=lambda p: p.info.priority.value)

    def execute_pipeline(
        self,
        data: Any,
        plugin_types: Optional[List[PluginType]] = None,
    ) -> Any:
        """Execute plugins in pipeline."""
        types = plugin_types or [
            PluginType.PREPROCESSOR,
            PluginType.ANALYZER,
            PluginType.POSTPROCESSOR,
        ]

        result = data
        for ptype in types:
            for plugin in self.get_plugins_by_type(ptype):
                result = plugin.execute(result)

        return result

    def list_plugins(self) -> List[PluginInfo]:
        """List all registered plugins."""
        return [p.info for p in self._plugins.values()]

    def cleanup_all(self) -> None:
        """Cleanup all plugins."""
        for plugin in self._plugins.values():
            plugin.cleanup()
        self._initialized.clear()


def create_simple_plugin(
    name: str,
    handler: Callable[[Any], Any],
    plugin_type: PluginType = PluginType.ANALYZER,
) -> Plugin:
    """Create a simple plugin from a function."""

    class SimplePlugin(Plugin):
        @property
        def info(self) -> PluginInfo:
            return PluginInfo(
                name=name,
                version="1.0.0",
                description=f"Simple {name} plugin",
                plugin_type=plugin_type,
            )

        def initialize(self, config: Dict[str, Any]) -> None:
            pass

        def execute(self, data: Any) -> Any:
            return handler(data)

    return SimplePlugin()
