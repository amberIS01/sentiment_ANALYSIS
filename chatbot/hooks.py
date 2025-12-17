"""
Hooks Module

Lifecycle hooks for sentiment analysis pipeline.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Dict, List, Any, Optional
from enum import Enum


class HookType(Enum):
    """Types of hooks."""

    PRE_ANALYSIS = "pre_analysis"
    POST_ANALYSIS = "post_analysis"
    ON_ERROR = "on_error"
    ON_POSITIVE = "on_positive"
    ON_NEGATIVE = "on_negative"
    ON_NEUTRAL = "on_neutral"


@dataclass
class HookContext:
    """Context passed to hooks."""

    hook_type: HookType
    data: Any
    metadata: Dict[str, Any]


HookFunction = Callable[[HookContext], Optional[Any]]


class HookManager:
    """Manage lifecycle hooks."""

    def __init__(self):
        """Initialize hook manager."""
        self._hooks: Dict[HookType, List[HookFunction]] = {
            hook_type: [] for hook_type in HookType
        }

    def register(
        self,
        hook_type: HookType,
        hook_func: HookFunction,
    ) -> None:
        """Register a hook function."""
        self._hooks[hook_type].append(hook_func)

    def unregister(
        self,
        hook_type: HookType,
        hook_func: HookFunction,
    ) -> bool:
        """Unregister a hook function."""
        if hook_func in self._hooks[hook_type]:
            self._hooks[hook_type].remove(hook_func)
            return True
        return False

    def trigger(
        self,
        hook_type: HookType,
        data: Any = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        """Trigger all hooks of a type."""
        context = HookContext(
            hook_type=hook_type,
            data=data,
            metadata=metadata or {},
        )

        results = []
        for hook_func in self._hooks[hook_type]:
            try:
                result = hook_func(context)
                results.append(result)
            except Exception as e:
                # Trigger error hooks
                if hook_type != HookType.ON_ERROR:
                    self.trigger(HookType.ON_ERROR, e)
                results.append(None)

        return results

    def clear(self, hook_type: Optional[HookType] = None) -> None:
        """Clear hooks."""
        if hook_type:
            self._hooks[hook_type].clear()
        else:
            for hooks in self._hooks.values():
                hooks.clear()

    def has_hooks(self, hook_type: HookType) -> bool:
        """Check if hooks are registered."""
        return len(self._hooks[hook_type]) > 0


def hook(hook_type: HookType):
    """Decorator to register a hook."""
    def decorator(func: HookFunction) -> HookFunction:
        func._hook_type = hook_type
        return func
    return decorator


class HookableMixin:
    """Mixin class to add hook support."""

    def __init__(self):
        self._hook_manager = HookManager()

    def add_hook(
        self,
        hook_type: HookType,
        hook_func: HookFunction,
    ) -> None:
        """Add a hook."""
        self._hook_manager.register(hook_type, hook_func)

    def remove_hook(
        self,
        hook_type: HookType,
        hook_func: HookFunction,
    ) -> bool:
        """Remove a hook."""
        return self._hook_manager.unregister(hook_type, hook_func)

    def trigger_hooks(
        self,
        hook_type: HookType,
        data: Any = None,
    ) -> List[Any]:
        """Trigger hooks."""
        return self._hook_manager.trigger(hook_type, data)


# Convenience functions
_default_manager = HookManager()


def register_hook(hook_type: HookType, func: HookFunction) -> None:
    """Register a hook with the default manager."""
    _default_manager.register(hook_type, func)


def trigger_hook(hook_type: HookType, data: Any = None) -> List[Any]:
    """Trigger hooks with the default manager."""
    return _default_manager.trigger(hook_type, data)
