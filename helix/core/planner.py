"""Task decomposition and planning engine"""

from typing import List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from helix.utils.logger import get_logger
from helix.utils.ollama_client import OllamaClient

logger = get_logger(__name__)


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class Task:
    """Represents a single task to be executed"""
    id: str
    description: str
    agent_type: str  # e.g., 'coder', 'research', 'automation'
    priority: TaskPriority = TaskPriority.MEDIUM
    dependencies: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"  # pending, running, completed, failed
    result: Any = None


class Planner:
    """Decomposes user requests into executable tasks"""

    def __init__(self, ollama_client: OllamaClient):
        self.ollama = ollama_client
        self.task_counter = 0

    async def decompose(self, user_request: str, context: Dict[str, Any] = None) -> List[Task]:
        """
        Decompose a user request into a list of tasks.
        Uses an LLM to intelligently break down complex requests.
        """
        context = context or {}
        
        prompt = self._build_decomposition_prompt(user_request, context)
        
        response = await self.ollama.generate(
            prompt=prompt,
            model="qwen:32b"
        )
        
        tasks = self._parse_task_list(response)
        logger.info(f"Decomposed request into {len(tasks)} tasks")
        return tasks

    def _build_decomposition_prompt(self, request: str, context: Dict[str, Any]) -> str:
        """
        Build a prompt for the LLM to decompose the request.
        """
        available_agents = "research, coder, automation, browser, vision, learning"
        
        return f"""
You are a task planning AI. Break down the following user request into a sequence of specific, actionable tasks.

User Request: {request}

Context: {context}

Available Agent Types: {available_agents}

For each task, specify:
1. A unique task ID (e.g., TASK_001)
2. Clear description of what needs to be done
3. Which agent should execute it
4. Priority (LOW, MEDIUM, HIGH, CRITICAL)
5. Dependencies (which tasks must complete first)

Format:
TASK_001: [description] | Agent: [type] | Priority: [level] | Dependencies: [list]

Provide the task breakdown:
"""

    def _parse_task_list(self, response: str) -> List[Task]:
        """
        Parse the LLM response into Task objects.
        """
        tasks = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or not line.startswith('TASK_'):
                continue
            
            try:
                # Parse: TASK_001: [description] | Agent: [type] | Priority: [level] | Dependencies: [list]
                parts = line.split('|')
                task_id = parts[0].split(':')[0].strip()
                description = parts[0].split(':')[1].strip()
                
                agent_type = parts[1].replace('Agent:', '').strip()
                priority_str = parts[2].replace('Priority:', '').strip()
                dependencies_str = parts[3].replace('Dependencies:', '').strip() if len(parts) > 3 else "[]"
                
                priority = TaskPriority[priority_str] if priority_str in TaskPriority.__members__ else TaskPriority.MEDIUM
                dependencies = [d.strip() for d in dependencies_str.strip('[]').split(',') if d.strip()]
                
                task = Task(
                    id=task_id,
                    description=description,
                    agent_type=agent_type,
                    priority=priority,
                    dependencies=dependencies
                )
                tasks.append(task)
            except Exception as e:
                logger.warning(f"Error parsing task line: {line} - {e}")
        
        return tasks

    def get_execution_order(self, tasks: List[Task]) -> List[Task]:
        """
        Determine optimal execution order based on dependencies and priority.
        Returns tasks in topologically sorted order.
        """
        # Simple topological sort
        visited = set()
        ordered = []
        
        def visit(task_id: str):
            if task_id in visited:
                return
            visited.add(task_id)
            
            task = next((t for t in tasks if t.id == task_id), None)
            if not task:
                return
            
            for dep_id in task.dependencies:
                visit(dep_id)
            
            ordered.append(task)
        
        for task in sorted(tasks, key=lambda t: t.priority.value, reverse=True):
            visit(task.id)
        
        return ordered
