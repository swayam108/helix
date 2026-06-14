"""Research agent for information gathering and summarization"""

from typing import Any, Dict
import asyncio

from helix.agents.base import BaseAgent
from helix.models.agent import AgentConfig, AgentType, AgentCapability
from helix.models.task import ExecutionTask, TaskOutput
from helix.utils.logger import get_logger
from helix.utils.ollama_client import OllamaClient

logger = get_logger(__name__)


class ResearchAgent(BaseAgent):
    """Agent specialized in research and information gathering"""

    def __init__(self, ollama_client: OllamaClient):
        config = AgentConfig(
            name="Research Agent",
            agent_type=AgentType.RESEARCH,
            description="Gathers and summarizes information from various sources",
            capabilities=[
                AgentCapability(
                    "web_research",
                    "Search and gather information from web sources",
                    input_types=["query"],
                    output_types=["summary", "sources"]
                ),
                AgentCapability(
                    "summarization",
                    "Summarize large amounts of text",
                    input_types=["text"],
                    output_types=["summary"]
                ),
                AgentCapability(
                    "knowledge_synthesis",
                    "Synthesize knowledge from multiple sources",
                    input_types=["documents"],
                    output_types=["synthesis"]
                ),
            ],
            required_permissions=["network.http", "filesystem.read"],
            preferred_model="llama2:latest",
        )
        super().__init__(config)
        self.ollama = ollama_client

    async def execute(self, task: ExecutionTask) -> TaskOutput:
        """
        Execute a research task.
        """
        task_type = task.metadata.get("type", "general_research")
        query = task.input.data.get("query", "") if task.input else ""

        logger.info(f"Research task: {task_type} - {query}")

        try:
            # Build research prompt
            prompt = f"""
You are a research assistant. Provide a comprehensive answer to the following query.
Include relevant details, sources (if applicable), and key findings.

Query: {query}

Response:
"""
            
            # Generate research using LLM
            response = await self.ollama.generate(
                prompt=prompt,
                model="llama2:latest",
                temperature=0.7
            )

            return TaskOutput(
                data={
                    "research_result": response,
                    "query": query,
                    "type": task_type
                },
                metadata={"agent": self.name, "model": "llama2"}
            )

        except Exception as e:
            logger.error(f"Research task failed: {e}")
            return TaskOutput(
                data={},
                errors=[str(e)]
            )

    def validate_task(self, task: ExecutionTask) -> bool:
        """
        Validate that this is a research task.
        """
        return task.agent_type == self.agent_type.value or "research" in task.description.lower()
