"""
State Machine Module

Conversation state management.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any, Set
from enum import Enum, auto


class ConversationState(Enum):
    """Default conversation states."""

    IDLE = auto()
    GREETING = auto()
    LISTENING = auto()
    PROCESSING = auto()
    RESPONDING = auto()
    FAREWELL = auto()
    ERROR = auto()


@dataclass
class Transition:
    """State transition definition."""

    from_state: Any
    to_state: Any
    trigger: str
    condition: Optional[Callable[[], bool]] = None
    action: Optional[Callable[[], None]] = None


@dataclass
class StateContext:
    """Context for state actions."""

    current_state: Any
    previous_state: Optional[Any]
    trigger: str
    data: Dict[str, Any] = field(default_factory=dict)


class StateMachine:
    """Finite state machine for conversations."""

    def __init__(self, initial_state: Any):
        """Initialize state machine."""
        self._state = initial_state
        self._previous_state: Optional[Any] = None
        self._transitions: Dict[Any, Dict[str, Transition]] = {}
        self._on_enter: Dict[Any, List[Callable]] = {}
        self._on_exit: Dict[Any, List[Callable]] = {}
        self._history: List[Any] = [initial_state]

    @property
    def state(self) -> Any:
        """Get current state."""
        return self._state

    @property
    def previous_state(self) -> Optional[Any]:
        """Get previous state."""
        return self._previous_state

    def add_transition(
        self,
        from_state: Any,
        to_state: Any,
        trigger: str,
        condition: Optional[Callable[[], bool]] = None,
        action: Optional[Callable[[], None]] = None,
    ) -> None:
        """Add a state transition."""
        if from_state not in self._transitions:
            self._transitions[from_state] = {}

        self._transitions[from_state][trigger] = Transition(
            from_state=from_state,
            to_state=to_state,
            trigger=trigger,
            condition=condition,
            action=action,
        )

    def on_enter(self, state: Any, callback: Callable) -> None:
        """Register callback for entering a state."""
        if state not in self._on_enter:
            self._on_enter[state] = []
        self._on_enter[state].append(callback)

    def on_exit(self, state: Any, callback: Callable) -> None:
        """Register callback for exiting a state."""
        if state not in self._on_exit:
            self._on_exit[state] = []
        self._on_exit[state].append(callback)

    def trigger(self, event: str) -> bool:
        """Trigger a state transition."""
        if self._state not in self._transitions:
            return False

        if event not in self._transitions[self._state]:
            return False

        transition = self._transitions[self._state][event]

        # Check condition
        if transition.condition and not transition.condition():
            return False

        # Exit callbacks
        for callback in self._on_exit.get(self._state, []):
            callback()

        # Execute action
        if transition.action:
            transition.action()

        # Update state
        self._previous_state = self._state
        self._state = transition.to_state
        self._history.append(self._state)

        # Enter callbacks
        for callback in self._on_enter.get(self._state, []):
            callback()

        return True

    def can_trigger(self, event: str) -> bool:
        """Check if event can be triggered."""
        if self._state not in self._transitions:
            return False
        return event in self._transitions[self._state]

    def get_available_triggers(self) -> List[str]:
        """Get available triggers for current state."""
        if self._state not in self._transitions:
            return []
        return list(self._transitions[self._state].keys())

    def reset(self, initial_state: Any) -> None:
        """Reset to initial state."""
        self._state = initial_state
        self._previous_state = None
        self._history = [initial_state]

    def get_history(self) -> List[Any]:
        """Get state history."""
        return self._history.copy()


class ConversationStateMachine(StateMachine):
    """Pre-configured state machine for conversations."""

    def __init__(self):
        """Initialize conversation state machine."""
        super().__init__(ConversationState.IDLE)
        self._setup_transitions()

    def _setup_transitions(self) -> None:
        """Set up default transitions."""
        self.add_transition(
            ConversationState.IDLE,
            ConversationState.GREETING,
            "greet",
        )
        self.add_transition(
            ConversationState.GREETING,
            ConversationState.LISTENING,
            "listen",
        )
        self.add_transition(
            ConversationState.LISTENING,
            ConversationState.PROCESSING,
            "process",
        )
        self.add_transition(
            ConversationState.PROCESSING,
            ConversationState.RESPONDING,
            "respond",
        )
        self.add_transition(
            ConversationState.RESPONDING,
            ConversationState.LISTENING,
            "continue",
        )
        self.add_transition(
            ConversationState.RESPONDING,
            ConversationState.FAREWELL,
            "goodbye",
        )
        self.add_transition(
            ConversationState.FAREWELL,
            ConversationState.IDLE,
            "reset",
        )
