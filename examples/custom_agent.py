"""Example: Creating a custom agent"""

from helix.agents.base import BaseAgent
from helix.models.agent import AgentConfig, AgentType, AgentCapability
from helix.models.task import ExecutionTask, TaskOutput
from helix.utils.logger import get_logger

logger = get_logger(__name__)


class DataAnalysisAgent(BaseAgent):
    """Example custom agent for data analysis"""

    def __init__(self):
        config = AgentConfig(
            name="Data Analysis Agent",
            agent_type=AgentType.LEARNING,
            description="Analyzes data and generates insights",
            capabilities=[
                AgentCapability(
                    "statistical_analysis",
                    "Perform statistical analysis on data",
                    input_types=["csv_data"],
                    output_types=["statistics", "insights"]
                ),
            ],
            required_permissions=["filesystem.read"],
            preferred_model="qwen:32b",
        )
        super().__init__(config)

    async def execute(self, task: ExecutionTask) -> TaskOutput:
        """Execute a data analysis task"""
        logger.info(f"Analyzing data for task {task.id}")
        
        # Get input data
        data = task.input.data if task.input else {}
        dataset = data.get("dataset", [])
        
        # Perform analysis
        analysis_results = {
            "count": len(dataset),
            "average": sum(dataset) / len(dataset) if dataset else 0,
            "min": min(dataset) if dataset else None,
            "max": max(dataset) if dataset else None,
        }
        
        return TaskOutput(
            data={"analysis": analysis_results},
            metadata={"agent": self.name, "analysis_type": "statistical"}
        )

    def validate_task(self, task: ExecutionTask) -> bool:
        """Validate that this is a data analysis task"""
        return "analysis" in task.description.lower() or "data" in task.description.lower()


if __name__ == "__main__":
    import asyncio
    from helix.models.task import ExecutionTask, TaskInput
    
    async def main():
        agent = DataAnalysisAgent()
        
        # Create a sample task
        task = ExecutionTask(
            id="ANALYSIS_001",
            description="Analyze the dataset",
            agent_type="learning",
            input=TaskInput(data={"dataset": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
        )
        
        # Execute the task
        result = await agent.run_task(task)
        print(f"Analysis Result: {result.output}")
    
    asyncio.run(main())
