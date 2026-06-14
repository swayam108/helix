"""Message models for inter-agent communication"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime
from enum import Enum


class MessageType(Enum):
    """Types of messages between agents"""
    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"
    ERROR = "error"
    STATUS = "status"


@dataclass
class Message:
    """Message between agents"""
    message_id: str
    sender: str
    receiver: str
    message_type: MessageType
    content: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    priority: int = 0
    requires_response: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MessageResponse:
    """Response to a message"""
    original_message_id: str
    sender: str
    receiver: str
    status: str  # "success", "error", "pending"
    result: Any = None
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
