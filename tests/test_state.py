"""
Tests for the State Module.
"""

import pytest

from chatbot.state import (
    StateMachine,
    ConversationStateMachine,
    ConversationState,
    Transition,
    StateContext,
)


class TestConversationState:
    """Test ConversationState enum."""

    def test_states_exist(self):
        assert ConversationState.IDLE is not None
        assert ConversationState.GREETING is not None
        assert ConversationState.LISTENING is not None


class TestStateMachine:
    """Test StateMachine class."""

    def test_initialization(self):
        sm = StateMachine(initial_state="start")
        assert sm.state == "start"

    def test_add_transition(self):
        sm = StateMachine(initial_state="a")
        sm.add_transition("a", "b", "go")
        assert sm.can_trigger("go") is True

    def test_trigger(self):
        sm = StateMachine(initial_state="a")
        sm.add_transition("a", "b", "go")
        result = sm.trigger("go")
        assert result is True
        assert sm.state == "b"

    def test_trigger_invalid(self):
        sm = StateMachine(initial_state="a")
        result = sm.trigger("invalid")
        assert result is False
        assert sm.state == "a"

    def test_previous_state(self):
        sm = StateMachine(initial_state="a")
        sm.add_transition("a", "b", "go")
        sm.trigger("go")
        assert sm.previous_state == "a"

    def test_on_enter(self):
        sm = StateMachine(initial_state="a")
        entered = []
        sm.add_transition("a", "b", "go")
        sm.on_enter("b", lambda: entered.append("b"))
        sm.trigger("go")
        assert entered == ["b"]

    def test_on_exit(self):
        sm = StateMachine(initial_state="a")
        exited = []
        sm.add_transition("a", "b", "go")
        sm.on_exit("a", lambda: exited.append("a"))
        sm.trigger("go")
        assert exited == ["a"]

    def test_can_trigger(self):
        sm = StateMachine(initial_state="a")
        sm.add_transition("a", "b", "go")
        assert sm.can_trigger("go") is True
        assert sm.can_trigger("stay") is False

    def test_get_available_triggers(self):
        sm = StateMachine(initial_state="a")
        sm.add_transition("a", "b", "go")
        sm.add_transition("a", "c", "jump")
        triggers = sm.get_available_triggers()
        assert "go" in triggers
        assert "jump" in triggers

    def test_reset(self):
        sm = StateMachine(initial_state="a")
        sm.add_transition("a", "b", "go")
        sm.trigger("go")
        sm.reset("a")
        assert sm.state == "a"
        assert sm.previous_state is None

    def test_get_history(self):
        sm = StateMachine(initial_state="a")
        sm.add_transition("a", "b", "go")
        sm.add_transition("b", "c", "next")
        sm.trigger("go")
        sm.trigger("next")
        history = sm.get_history()
        assert history == ["a", "b", "c"]


class TestConversationStateMachine:
    """Test ConversationStateMachine class."""

    def test_initialization(self):
        sm = ConversationStateMachine()
        assert sm.state == ConversationState.IDLE

    def test_greet_transition(self):
        sm = ConversationStateMachine()
        sm.trigger("greet")
        assert sm.state == ConversationState.GREETING

    def test_full_flow(self):
        sm = ConversationStateMachine()
        sm.trigger("greet")
        sm.trigger("listen")
        sm.trigger("process")
        sm.trigger("respond")
        assert sm.state == ConversationState.RESPONDING
