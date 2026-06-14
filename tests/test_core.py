"""Tests for core HELIX functionality"""

import pytest
import asyncio
from helix.core.commander import Commander
from helix.core.planner import Planner, Task, TaskPriority
from helix.core.memory import Memory
from helix.core.event_bus import EventBus, Event
from helix.utils.ollama_client import OllamaClient


@pytest.fixture
def event_bus():
    """Create an EventBus for testing"""
    return EventBus()


@pytest.fixture
def memory():
    """Create a Memory instance for testing"""
    return Memory(":memory:")  # Use in-memory SQLite


@pytest.fixture
def ollama_client():
    """Create an OllamaClient for testing"""
    return OllamaClient()


class TestEventBus:
    """Test event bus functionality"""

    @pytest.mark.asyncio
    async def test_publish_subscribe(self, event_bus):
        """Test basic publish/subscribe"""
        received_events = []

        async def subscriber(event: Event):
            received_events.append(event)

        event_bus.subscribe("test_event", subscriber)

        event = Event(type="test_event", sender="test", data={"key": "value"})
        await event_bus.publish(event)

        assert len(received_events) == 1
        assert received_events[0].type == "test_event"

    def test_event_history(self, event_bus):
        """Test event history tracking"""
        event = Event(type="test", sender="test", data={})
        asyncio.run(event_bus.publish(event))

        history = event_bus.get_history()
        assert len(history) > 0
        assert history[-1].type == "test"


class TestMemory:
    """Test memory system"""

    def test_store_retrieve(self, memory):
        """Test storing and retrieving data"""
        memory.store("test_key", {"data": "value"}, category="test")
        retrieved = memory.retrieve("test_key")

        assert retrieved is not None
        assert retrieved["data"] == "value"

    def test_search_by_category(self, memory):
        """Test searching by category"""
        memory.store("key1", "value1", category="test")
        memory.store("key2", "value2", category="test")
        memory.store("key3", "value3", category="other")

        results = memory.search("test")
        assert len(results) >= 2


class TestPlanner:
    """Test task planning"""

    @pytest.mark.asyncio
    async def test_task_decomposition(self, ollama_client):
        """Test breaking down user requests into tasks"""
        planner = Planner(ollama_client)
        
        # This test would require Ollama to be running
        # For now, just test the structure
        assert planner is not None
        assert hasattr(planner, 'decompose')

    def test_execution_order(self, ollama_client):
        """Test task dependency resolution"""
        planner = Planner(ollama_client)
        
        tasks = [
            Task(id="TASK_001", description="Task 1", agent_type="research"),
            Task(id="TASK_002", description="Task 2", agent_type="coder", dependencies=["TASK_001"]),
            Task(id="TASK_003", description="Task 3", agent_type="automation", dependencies=["TASK_002"]),
        ]
        
        ordered = planner.get_execution_order(tasks)
        assert len(ordered) == 3
        assert ordered[0].id == "TASK_001"
        assert ordered[1].id == "TASK_002"
        assert ordered[2].id == "TASK_003"


class TestCommander:
    """Test main orchestration engine"""

    def test_commander_initialization(self):
        """Test Commander initialization"""
        commander = Commander()
        assert commander is not None
        assert hasattr(commander, 'memory')
        assert hasattr(commander, 'executor')
        assert hasattr(commander, 'planner')

    def test_system_status(self):
        """Test getting system status"""
        commander = Commander()
        status = commander.get_system_status()
        
        assert "status" in status
        assert "cpu_percent" in status
        assert "memory_percent" in status


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
