"""Event-based communication system for agents"""

import asyncio
from typing import Any, Callable, Dict, List
from dataclasses import dataclass, field
from datetime import datetime
from helix.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Event:
    """Represents a communication event between agents"""
    type: str
    sender: str
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    priority: int = 0  # Higher = more urgent


class EventBus:
    """Central event bus for inter-agent communication"""

    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_queue: asyncio.Queue = asyncio.Queue()
        self.event_history: List[Event] = []
        self.max_history = 10000

    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe to a specific event type"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to {event_type}: {callback.__name__}")

    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Unsubscribe from an event type"""
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(callback)

    async def publish(self, event: Event) -> None:
        """Publish an event to all subscribers"""
        self.event_history.append(event)
        if len(self.event_history) > self.max_history:
            self.event_history.pop(0)

        logger.debug(f"Event published: {event.type} from {event.sender}")

        if event.type in self.subscribers:
            for callback in self.subscribers[event.type]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(event)
                    else:
                        callback(event)
                except Exception as e:
                    logger.error(f"Error in event callback: {e}")

    def get_history(self, event_type: str = None, limit: int = 100) -> List[Event]:
        """Get event history, optionally filtered by type"""
        history = self.event_history[-limit:]
        if event_type:
            history = [e for e in history if e.type == event_type]
        return history
