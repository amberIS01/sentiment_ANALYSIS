"""
Conversation Flow Module

Manage conversation flow and transitions.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
from enum import Enum, auto


class FlowState(Enum):
    """Flow states."""

    START = auto()
    GREETING = auto()
    MAIN = auto()
    CLARIFY = auto()
    CONFIRM = auto()
    END = auto()


@dataclass
class FlowTransition:
    """A transition between states."""

    from_state: FlowState
    to_state: FlowState
    condition: Optional[Callable[[str], bool]] = None
    action: Optional[Callable[[str], str]] = None


@dataclass
class FlowContext:
    """Context for the current flow."""

    state: FlowState
    user_input: str
    variables: Dict[str, Any] = field(default_factory=dict)
    history: List[str] = field(default_factory=list)


class ConversationFlow:
    """Manage conversation flow."""

    def __init__(self):
        self._state = FlowState.START
        self._transitions: Dict[FlowState, List[FlowTransition]] = {}
        self._handlers: Dict[FlowState, Callable[[str], str]] = {}
        self._variables: Dict[str, Any] = {}
        self._history: List[str] = []
        self._setup_default_handlers()

    def _setup_default_handlers(self) -> None:
        """Set up default state handlers."""
        self._handlers[FlowState.START] = self._handle_start
        self._handlers[FlowState.GREETING] = self._handle_greeting
        self._handlers[FlowState.MAIN] = self._handle_main
        self._handlers[FlowState.END] = self._handle_end

    def _handle_start(self, user_input: str) -> str:
        self._state = FlowState.GREETING
        return "Hello! How can I help you today?"

    def _handle_greeting(self, user_input: str) -> str:
        self._state = FlowState.MAIN
        return "I'm ready to analyze sentiment. What would you like to discuss?"

    def _handle_main(self, user_input: str) -> str:
        if any(word in user_input.lower() for word in ["bye", "goodbye", "exit"]):
            self._state = FlowState.END
            return "Goodbye! Have a great day!"
        return "I understand. Tell me more about how you feel."

    def _handle_end(self, user_input: str) -> str:
        return "The conversation has ended. Say hello to start a new one."

    def add_transition(
        self,
        from_state: FlowState,
        to_state: FlowState,
        condition: Optional[Callable[[str], bool]] = None,
    ) -> None:
        """Add a transition between states."""
        if from_state not in self._transitions:
            self._transitions[from_state] = []

        self._transitions[from_state].append(FlowTransition(
            from_state=from_state,
            to_state=to_state,
            condition=condition,
        ))

    def set_handler(
        self,
        state: FlowState,
        handler: Callable[[str], str],
    ) -> None:
        """Set handler for a state."""
        self._handlers[state] = handler

    def process(self, user_input: str) -> str:
        """Process user input and return response."""
        self._history.append(user_input)

        # Check for transitions
        if self._state in self._transitions:
            for transition in self._transitions[self._state]:
                if transition.condition is None or transition.condition(user_input):
                    self._state = transition.to_state
                    if transition.action:
                        return transition.action(user_input)
                    break

        # Use state handler
        handler = self._handlers.get(self._state, self._handle_main)
        return handler(user_input)

    def set_variable(self, key: str, value: Any) -> None:
        """Set a flow variable."""
        self._variables[key] = value

    def get_variable(self, key: str, default: Any = None) -> Any:
        """Get a flow variable."""
        return self._variables.get(key, default)

    def reset(self) -> None:
        """Reset to initial state."""
        self._state = FlowState.START
        self._variables.clear()
        self._history.clear()

    @property
    def state(self) -> FlowState:
        """Get current state."""
        return self._state

    @property
    def history(self) -> List[str]:
        """Get conversation history."""
        return self._history.copy()


def create_flow() -> ConversationFlow:
    """Create a new conversation flow."""
    return ConversationFlow()
