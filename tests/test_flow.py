"""Tests for flow module."""

import pytest
from chatbot.flow import (
    FlowState,
    FlowTransition,
    ConversationFlow,
    FlowManager,
    create_flow,
)


class TestConversationFlow:
    """Tests for ConversationFlow."""

    def test_create(self):
        """Test creating flow."""
        flow = ConversationFlow(
            name="test_flow",
            initial_state=FlowState.GREETING,
        )
        
        assert flow.name == "test_flow"
        assert flow.current_state == FlowState.GREETING

    def test_add_transition(self):
        """Test adding transition."""
        flow = ConversationFlow("test", FlowState.GREETING)
        flow.add_transition(
            FlowState.GREETING,
            FlowState.LISTENING,
            "user_input",
        )
        
        assert len(flow.transitions) == 1

    def test_transition(self):
        """Test state transition."""
        flow = ConversationFlow("test", FlowState.GREETING)
        flow.add_transition(FlowState.GREETING, FlowState.LISTENING, "input")
        
        result = flow.transition("input")
        
        assert result is True
        assert flow.current_state == FlowState.LISTENING

    def test_invalid_transition(self):
        """Test invalid transition."""
        flow = ConversationFlow("test", FlowState.GREETING)
        
        result = flow.transition("invalid")
        
        assert result is False

    def test_reset(self):
        """Test resetting flow."""
        flow = ConversationFlow("test", FlowState.GREETING)
        flow.add_transition(FlowState.GREETING, FlowState.LISTENING, "input")
        flow.transition("input")
        
        flow.reset()
        
        assert flow.current_state == FlowState.GREETING


class TestFlowManager:
    """Tests for FlowManager."""

    def test_register_flow(self):
        """Test registering flow."""
        manager = FlowManager()
        flow = ConversationFlow("test", FlowState.GREETING)
        
        manager.register(flow)
        
        assert manager.get_flow("test") is not None

    def test_unregister_flow(self):
        """Test unregistering flow."""
        manager = FlowManager()
        flow = ConversationFlow("test", FlowState.GREETING)
        manager.register(flow)
        
        result = manager.unregister("test")
        
        assert result is True
        assert manager.get_flow("test") is None

    def test_get_active_flows(self):
        """Test getting active flows."""
        manager = FlowManager()
        manager.register(ConversationFlow("a", FlowState.GREETING))
        manager.register(ConversationFlow("b", FlowState.LISTENING))
        
        active = manager.get_active_flows()
        
        assert len(active) == 2

    def test_reset_all(self):
        """Test resetting all flows."""
        manager = FlowManager()
        flow = ConversationFlow("test", FlowState.GREETING)
        flow.add_transition(FlowState.GREETING, FlowState.LISTENING, "x")
        flow.transition("x")
        manager.register(flow)
        
        manager.reset_all()
        
        assert flow.current_state == FlowState.GREETING


class TestCreateFlow:
    """Tests for create_flow function."""

    def test_create(self):
        """Test creating flow."""
        flow = create_flow("simple", FlowState.GREETING)
        
        assert flow.name == "simple"

    def test_create_with_transitions(self):
        """Test creating with transitions."""
        transitions = [
            (FlowState.GREETING, FlowState.LISTENING, "start"),
            (FlowState.LISTENING, FlowState.RESPONDING, "process"),
        ]
        
        flow = create_flow("complex", FlowState.GREETING, transitions)
        
        assert len(flow.transitions) == 2
