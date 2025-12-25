"""
Tests for the Hooks Module.
"""

import pytest

from chatbot.hooks import (
    HookManager,
    HookType,
    HookContext,
    HookableMixin,
    hook,
    register_hook,
    trigger_hook,
)


class TestHookType:
    """Test HookType enum."""

    def test_values(self):
        assert HookType.PRE_ANALYSIS.value == "pre_analysis"
        assert HookType.POST_ANALYSIS.value == "post_analysis"
        assert HookType.ON_ERROR.value == "on_error"


class TestHookContext:
    """Test HookContext dataclass."""

    def test_creation(self):
        ctx = HookContext(
            hook_type=HookType.PRE_ANALYSIS,
            data="test",
            metadata={"key": "value"},
        )
        assert ctx.hook_type == HookType.PRE_ANALYSIS
        assert ctx.data == "test"


class TestHookManager:
    """Test HookManager class."""

    def test_initialization(self):
        manager = HookManager()
        assert manager is not None

    def test_register(self):
        manager = HookManager()
        manager.register(HookType.PRE_ANALYSIS, lambda ctx: None)
        assert manager.has_hooks(HookType.PRE_ANALYSIS) is True

    def test_unregister(self):
        manager = HookManager()
        func = lambda ctx: None
        manager.register(HookType.PRE_ANALYSIS, func)
        result = manager.unregister(HookType.PRE_ANALYSIS, func)
        assert result is True
        assert manager.has_hooks(HookType.PRE_ANALYSIS) is False

    def test_trigger(self):
        manager = HookManager()
        results = []
        manager.register(HookType.PRE_ANALYSIS, lambda ctx: results.append(ctx.data))
        manager.trigger(HookType.PRE_ANALYSIS, data="test")
        assert results == ["test"]

    def test_trigger_multiple(self):
        manager = HookManager()
        results = []
        manager.register(HookType.PRE_ANALYSIS, lambda ctx: results.append(1))
        manager.register(HookType.PRE_ANALYSIS, lambda ctx: results.append(2))
        manager.trigger(HookType.PRE_ANALYSIS)
        assert results == [1, 2]

    def test_clear_specific(self):
        manager = HookManager()
        manager.register(HookType.PRE_ANALYSIS, lambda ctx: None)
        manager.register(HookType.POST_ANALYSIS, lambda ctx: None)
        manager.clear(HookType.PRE_ANALYSIS)
        assert manager.has_hooks(HookType.PRE_ANALYSIS) is False
        assert manager.has_hooks(HookType.POST_ANALYSIS) is True

    def test_clear_all(self):
        manager = HookManager()
        manager.register(HookType.PRE_ANALYSIS, lambda ctx: None)
        manager.register(HookType.POST_ANALYSIS, lambda ctx: None)
        manager.clear()
        assert manager.has_hooks(HookType.PRE_ANALYSIS) is False
        assert manager.has_hooks(HookType.POST_ANALYSIS) is False


class TestHookableMixin:
    """Test HookableMixin class."""

    def test_add_hook(self):
        class MyClass(HookableMixin):
            pass

        obj = MyClass()
        obj.add_hook(HookType.PRE_ANALYSIS, lambda ctx: None)
        assert obj._hook_manager.has_hooks(HookType.PRE_ANALYSIS)

    def test_trigger_hooks(self):
        class MyClass(HookableMixin):
            pass

        obj = MyClass()
        results = []
        obj.add_hook(HookType.PRE_ANALYSIS, lambda ctx: results.append(1))
        obj.trigger_hooks(HookType.PRE_ANALYSIS)
        assert results == [1]


class TestHookDecorator:
    """Test hook decorator."""

    def test_marks_function(self):
        @hook(HookType.PRE_ANALYSIS)
        def my_hook(ctx):
            pass

        assert my_hook._hook_type == HookType.PRE_ANALYSIS
