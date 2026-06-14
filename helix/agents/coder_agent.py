"""Coder agent for code generation and debugging"""

from typing import Any, Dict
import asyncio

from helix.agents.base import BaseAgent
from helix.models.agent import AgentConfig, AgentType, AgentCapability
from helix.models.task import ExecutionTask, TaskOutput
from helix.utils.logger import get_logger
from helix.utils.ollama_client import OllamaClient

logger = get_logger(__name__)


class CoderAgent(BaseAgent):
    """Agent specialized in code generation and debugging"""

    def __init__(self, ollama_client: OllamaClient):
        config = AgentConfig(
            name="Coder Agent",
            agent_type=AgentType.CODER,
            description="Generates, debugs, and optimizes code",
            capabilities=[
                AgentCapability(
                    "code_generation",
                    "Generate code based on specifications",
                    input_types=["specification"],
                    output_types=["code"]
                ),
                AgentCapability(
                    "debugging",
                    "Debug and fix code issues",
                    input_types=["code", "error"],
                    output_types=["fixed_code"]
                ),
                AgentCapability(
                    "code_review",
                    "Review code for quality and best practices",
                    input_types=["code"],
                    output_types=["review", "suggestions"]
                ),
            ],
            required_permissions=["filesystem.read", "filesystem.write", "code.execute"],
            preferred_model="deepseek-coder:33b",
        )
        super().__init__(config)
        self.ollama = ollama_client

    async def execute(self, task: ExecutionTask) -> TaskOutput:
        """
        Execute a coding task.
        """
        task_type = task.metadata.get("type", "code_generation")
        specification = task.input.data.get("specification", "") if task.input else ""
        language = task.input.data.get("language", "python") if task.input else "python"

        logger.info(f"Coding task: {task_type} - Language: {language}")

        try:
            # Build coding prompt
            prompt = f"""
You are an expert programmer. Generate high-quality {language} code based on the following specification.
Include comments and follow best practices.

Specification: {specification}

Code:
```{language}
"""

            # Generate code using LLM
            response = await self.ollama.generate(
                prompt=prompt,
                model="deepseek-coder:33b",
                temperature=0.3
            )

            return TaskOutput(
                data={
                    "code": response,
                    "language": language,
                    "type": task_type
                },
                metadata={"agent": self.name, "model": "deepseek-coder"}
            )

        except Exception as e:
            logger.error(f"Coding task failed: {e}")
            return TaskOutput(
                data={},
                errors=[str(e)]
            )

    def validate_task(self, task: ExecutionTask) -> bool:
        """
        Validate that this is a coding task.
        """
        return task.agent_type == self.agent_type.value or "code" in task.description.lower()
