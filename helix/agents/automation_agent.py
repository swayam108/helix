"""Automation agent for system operations and workflows"""

from typing import Any, Dict
import asyncio
import subprocess

from helix.agents.base import BaseAgent
from helix.models.agent import AgentConfig, AgentType, AgentCapability
from helix.models.task import ExecutionTask, TaskOutput
from helix.utils.logger import get_logger
from helix.utils.ollama_client import OllamaClient
from helix.utils.safety import SafetyManager

logger = get_logger(__name__)


class AutomationAgent(BaseAgent):
    """Agent specialized in system automation and file operations"""

    def __init__(self, ollama_client: OllamaClient, safety_manager: SafetyManager):
        config = AgentConfig(
            name="Automation Agent",
            agent_type=AgentType.AUTOMATION,
            description="Automates system operations, file handling, and workflows",
            capabilities=[
                AgentCapability(
                    "file_operations",
                    "Read, write, and manage files",
                    input_types=["file_path", "content"],
                    output_types=["success", "file_content"]
                ),
                AgentCapability(
                    "system_commands",
                    "Execute system commands (with restrictions)",
                    input_types=["command"],
                    output_types=["output", "status"]
                ),
                AgentCapability(
                    "workflow_automation",
                    "Create and execute automated workflows",
                    input_types=["workflow_definition"],
                    output_types=["workflow_result"]
                ),
            ],
            required_permissions=["filesystem.read", "filesystem.write", "system.execute"],
            preferred_model="deepseek-r1:32b",
        )
        super().__init__(config)
        self.ollama = ollama_client
        self.safety = safety_manager

    async def execute(self, task: ExecutionTask) -> TaskOutput:
        """
        Execute an automation task.
        """
        task_type = task.metadata.get("type", "general_automation")
        operation = task.input.data.get("operation", "") if task.input else ""

        logger.info(f"Automation task: {task_type} - Operation: {operation}")

        try:
            # Check permissions
            if not self.safety.has_permission(
                self.name, "system", "execute"
            ):
                return TaskOutput(
                    data={},
                    errors=["Permission denied: system execution not allowed"]
                )

            # Execute operation
            if task_type == "file_read":
                result = await self._file_read(operation)
            elif task_type == "file_write":
                result = await self._file_write(
                    operation,
                    task.input.data.get("content", "")
                )
            elif task_type == "system_command":
                result = await self._execute_command(operation)
            else:
                result = {"status": "unknown_operation"}

            return TaskOutput(
                data=result,
                metadata={"agent": self.name, "type": task_type}
            )

        except Exception as e:
            logger.error(f"Automation task failed: {e}")
            return TaskOutput(
                data={},
                errors=[str(e)]
            )

    async def _file_read(self, filepath: str) -> Dict[str, Any]:
        """Read a file safely"""
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            return {
                "status": "success",
                "content": content,
                "filepath": filepath
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _file_write(self, filepath: str, content: str) -> Dict[str, Any]:
        """Write to a file safely"""
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            return {
                "status": "success",
                "filepath": filepath,
                "bytes_written": len(content)
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _execute_command(self, command: str) -> Dict[str, Any]:
        """Execute a system command with safety checks"""
        logger.warning(f"System command execution requested: {command}")
        return {
            "status": "denied",
            "message": "Direct command execution disabled for safety",
            "command": command
        }

    def validate_task(self, task: ExecutionTask) -> bool:
        """
        Validate that this is an automation task.
        """
        return task.agent_type == self.agent_type.value or "automat" in task.description.lower()
