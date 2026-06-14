"""Agent base class and interface"""

import asyncio
from typing import Any, Dict, Optional, List
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from helix.models.agent import AgentConfig, AgentType
from helix.models.task import ExecutionTask, TaskStatus
from helix.utils.logger import get_logger

logger = get_logger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all agents in HELIX.
    Defines the interface that all agents must implement.
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self.name = config.name
        self.agent_type = config.agent_type
        self.description = config.description
        self.capabilities = config.capabilities
        self.running_tasks: Dict[str, ExecutionTask] = {}
        self.completed_tasks: List[ExecutionTask] = []
        self.failed_tasks: List[ExecutionTask] = []
        self.created_at = datetime.now()

    @abstractmethod
    async def execute(self, task: ExecutionTask) -> Any:
        """
        Execute a task assigned to this agent.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def validate_task(self, task: ExecutionTask) -> bool:
        """
        Validate that this agent can execute the given task.
        """
        pass

    async def run_task(self, task: ExecutionTask) -> ExecutionTask:
        """
        Run a task with automatic error handling and tracking.
        """
        task.status = TaskStatus.RUNNING
        task.execution.start_time = datetime.now()
        self.running_tasks[task.id] = task

        try:
            logger.info(f"[{self.name}] Starting task {task.id}: {task.description}")

            # Execute the task
            result = await self.execute(task)
            
            task.output = result
            task.status = TaskStatus.COMPLETED
            logger.info(f"[{self.name}] Completed task {task.id}")

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.execution.last_error = str(e)
            logger.error(f"[{self.name}] Failed task {task.id}: {e}")
            self.failed_tasks.append(task)
            raise

        finally:
            task.execution.end_time = datetime.now()
            task.execution.duration_seconds = (
                task.execution.end_time - task.execution.start_time
            ).total_seconds()
            
            if task.id in self.running_tasks:
                del self.running_tasks[task.id]
            
            if task.status == TaskStatus.COMPLETED:
                self.completed_tasks.append(task)

        return task

    def get_status(self) -> Dict[str, Any]:
        """
        Get current agent status.
        """
        return {
            "name": self.name,
            "type": self.agent_type.value,
            "description": self.description,
            "running_tasks": len(self.running_tasks),
            "completed_tasks": len(self.completed_tasks),
            "failed_tasks": len(self.failed_tasks),
            "created_at": self.created_at.isoformat(),
            "capabilities": [c.name for c in self.capabilities],
        }

    def get_capability(self, name: str):
        """
        Get a specific capability by name.
        """
        for cap in self.capabilities:
            if cap.name == name:
                return cap
        return None
