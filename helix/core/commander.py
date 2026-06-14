"""Main orchestration engine"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from helix.core.planner import Planner, Task
from helix.core.executor import Executor
from helix.core.memory import Memory
from helix.core.event_bus import EventBus, Event
from helix.core.resource_monitor import ResourceMonitor
from helix.utils.logger import get_logger
from helix.utils.ollama_client import OllamaClient

logger = get_logger(__name__)


class CommandResult:
    """Result of command execution"""
    def __init__(self):
        self.status: str = "pending"  # pending, running, completed, failed
        self.output: Any = None
        self.tasks: List[Task] = []
        self.task_results: Dict[str, Any] = {}
        self.execution_time: float = 0.0
        self.errors: List[str] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None


class Commander:
    """Main orchestration engine - coordinates all agents and execution"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.event_bus = EventBus()
        self.memory = Memory()
        self.resource_monitor = ResourceMonitor()
        self.ollama = OllamaClient()
        self.planner = Planner(self.ollama)
        self.executor = Executor(self.event_bus)
        self.max_concurrent_agents = self.config.get("max_concurrent_agents", 5)
        self.results_history: List[CommandResult] = []

    async def execute(self, user_request: str, context: Dict[str, Any] = None) -> CommandResult:
        """
        Main execution flow: understand -> plan -> execute -> validate
        """
        result = CommandResult()
        result.status = "running"
        result.start_time = datetime.now()
        
        try:
            logger.info(f"Commander received request: {user_request}")
            
            # Step 1: Get context from memory
            context = context or {}
            stored_context = self.memory.retrieve("user_context")
            if stored_context:
                context.update(stored_context)
            
            # Step 2: Check resources
            resource_status = self.resource_monitor.get_usage()
            logger.info(f"Resource status: CPU={resource_status.cpu_percent:.1f}%, "
                       f"Memory={resource_status.memory_percent:.1f}%")
            
            # Step 3: Decompose request into tasks
            logger.info("Planning phase: decomposing request...")
            tasks = await self.planner.decompose(user_request, context)
            result.tasks = tasks
            
            if not tasks:
                raise ValueError("No tasks generated from user request")
            
            # Step 4: Order tasks by dependencies
            ordered_tasks = self.planner.get_execution_order(tasks)
            logger.info(f"Task order determined: {[t.id for t in ordered_tasks]}")
            
            # Step 5: Execute tasks
            logger.info("Execution phase: running tasks...")
            task_results = await self.executor.execute_tasks(ordered_tasks)
            result.task_results = task_results
            
            # Step 6: Aggregate results
            result.output = self._aggregate_results(task_results)
            
            # Step 7: Store in memory
            self.memory.store(
                key=f"execution_{datetime.now().isoformat()}",
                value={
                    "request": user_request,
                    "tasks": [t.id for t in tasks],
                    "results": task_results
                },
                category="execution_history"
            )
            
            result.status = "completed"
            logger.info("Command execution completed successfully")
        
        except Exception as e:
            result.status = "failed"
            result.errors.append(str(e))
            logger.error(f"Command execution failed: {e}")
        
        finally:
            result.end_time = datetime.now()
            result.execution_time = (result.end_time - result.start_time).total_seconds()
            self.results_history.append(result)
        
        return result

    def _aggregate_results(self, task_results: Dict[str, Any]) -> str:
        """
        Aggregate task results into a final response.
        """
        output_parts = []
        for task_id, result in task_results.items():
            if isinstance(result, dict) and "error" in result:
                output_parts.append(f"⚠️ Task {task_id} failed: {result['error']}")
            else:
                output_parts.append(f"✓ Task {task_id}: {result}")
        
        return "\n".join(output_parts)

    def register_agent(self, agent_type: str, handler) -> None:
        """
        Register an agent handler with the executor.
        """
        self.executor.register_agent_handler(agent_type, handler)
        logger.info(f"Agent registered: {agent_type}")

    def get_system_status(self) -> Dict[str, Any]:
        """
        Get current system status.
        """
        resource_usage = self.resource_monitor.get_usage()
        return {
            "status": "running",
            "active_agents": len(self.executor.running_tasks),
            "completed_tasks": len(self.executor.completed_tasks),
            "cpu_percent": resource_usage.cpu_percent,
            "memory_percent": resource_usage.memory_percent,
            "memory_mb": resource_usage.memory_mb,
            "disk_percent": resource_usage.disk_percent,
        }

    def get_execution_history(self, limit: int = 10) -> List[CommandResult]:
        """
        Get recent execution history.
        """
        return self.results_history[-limit:]
