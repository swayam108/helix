"""Research task example"""

import asyncio
from helix.core.commander import Commander
from helix.agents.research_agent import ResearchAgent
from helix.utils.ollama_client import OllamaClient


async def main():
    """Run research example"""
    commander = Commander()
    
    # Initialize research agent
    ollama = OllamaClient()
    research_agent = ResearchAgent(ollama)
    
    # Register agent with commander
    commander.register_agent("research", research_agent.execute)
    
    # Execute research request
    research_request = """
    Research and summarize:
    1. What are the main differences between supervised and unsupervised learning?
    2. Provide practical examples of each approach
    3. List the pros and cons of each
    """
    
    print("\n=== Research Task ===")
    result = await commander.execute(research_request)
    
    print(f"Status: {result.status}")
    print(f"Execution Time: {result.execution_time:.2f}s")
    print("\nResearch Output:")
    print(result.output)


if __name__ == "__main__":
    asyncio.run(main())
