"""Task execution engine"""

import asyncio
from typing import Dict, List, Any, Callable
from helix.core.planner import Task, TaskPriority
from helix.core.event_bus import Event, EventBus
from helix.utils.logger import get_logger

logger = get_logger(__name__)


class Executor:
    """Manages task execution across agent pool"""

    def __init__(self, event_bus: EventBus, max_concurrent: int = 5):
        self.event_bus = event_bus
        self.max_concurrent = max_concurrent
        self.agent_handlers: Dict[str, Callable] = {}
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.completed_tasks: Dict[str, Any] = {}

    def register_agent_handler(self, agent_type: str, handler: Callable) -> None:
        """
        Register an executor function for a specific agent type.
        """
        self.agent_handlers[agent_type] = handler
        logger.debug(f"Registered handler for agent type: {agent_type}")

    async def execute_task(self, task: Task) -> Any:
        """
        Execute a single task using the appropriate agent.
        """
        logger.info(f"Executing task: {task.id} - {task.description}")
        
        task.status = "running"
        
        # Publish task started event
        await self.event_bus.publish(Event(
            type="task_started",
            sender="executor",
            data={"task_id": task.id, "agent_type": task.agent_type}
        ))
        
        try:
            handler = self.agent_handlers.get(task.agent_type)
            if not handler:
                raise ValueError(f"No handler for agent type: {task.agent_type}")
            
            if asyncio.iscoroutinefunction(handler):
                result = await handler(task)
            else:
                result = handler(task)
            
            task.status = "completed"
            task.result = result
            self.completed_tasks[task.id] = result
            
            # Publish task completed event
            await self.event_bus.publish(Event(
                type="task_completed",
                sender="executor",
                data={"task_id": task.id, "result": result}
            ))
            
            logger.info(f"Task completed: {task.id}")
            return result
        
        except Exception as e:
            task.status = "failed"
            logger.error(f"Task failed: {task.id} - {e}")
            
            # Publish task failed event
            await self.event_bus.publish(Event(
                type="task_failed",
                sender="executor",
                data={"task_id": task.id, "error": str(e)}
            ))
            
            raise

    async def execute_tasks(self, tasks: List[Task]) -> Dict[str, Any]:
        """
        Execute multiple tasks with dependency resolution.
        Returns a dict mapping task_id to result.
        """
        results = {}
        pending = {t.id: t for t in tasks}
        in_progress = {}
        
        while pending or in_progress:
            # Start new tasks if under concurrent limit
            if len(in_progress) < self.max_concurrent and pending:
                for task_id, task in list(pending.items()):
                    # Check if all dependencies are met
                    deps_met = all(dep in results for dep in task.dependencies)
                    if deps_met:
                        coro = self.execute_task(task)
                        in_progress[task_id] = asyncio.create_task(coro)
                        del pending[task_id]
            
            if not in_progress:
                break
            
            # Wait for at least one task to complete
            done, _ = await asyncio.wait(
                in_progress.values(),
                return_when=asyncio.FIRST_COMPLETED
            )
            
            for future in done:
                for task_id, task_future in list(in_progress.items()):
                    if task_future is future:
                        try:
                            result = await task_future
                            results[task_id] = result
                        except Exception as e:
                            logger.error(f"Task {task_id} failed: {e}")
                            results[task_id] = {"error": str(e)}
                        del in_progress[task_id]
        
        return results

    def get_task_result(self, task_id: str) -> Any:
        """
        Retrieve result of a completed task.
        """
        return self.completed_tasks.get(task_id)
