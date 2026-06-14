"""Agent models and definitions"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class AgentType(Enum):
    """Types of agents in the system"""
    COMMANDER = "commander"
    PLANNER = "planner"
    RESEARCH = "research"
    CODER = "coder"
    AUTOMATION = "automation"
    BROWSER = "browser"
    VISION = "vision"
    VOICE = "voice"
    MEMORY = "memory"
    SECURITY = "security"
    LEARNING = "learning"


@dataclass
class AgentCapability:
    """Describes what an agent can do"""
    name: str
    description: str
    input_types: List[str] = field(default_factory=list)
    output_types: List[str] = field(default_factory=list)


@dataclass
class AgentConfig:
    """Configuration for an agent"""
    name: str
    agent_type: AgentType
    description: str
    capabilities: List[AgentCapability] = field(default_factory=list)
    required_permissions: List[str] = field(default_factory=list)
    preferred_model: str = "qwen:32b"
    max_concurrent_tasks: int = 3
    timeout_seconds: int = 300
    retry_attempts: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)
