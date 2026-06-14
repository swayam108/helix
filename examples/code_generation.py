"""Code generation example"""

import asyncio
from helix.core.commander import Commander
from helix.agents.coder_agent import CoderAgent
from helix.utils.ollama_client import OllamaClient


async def main():
    """Run code generation example"""
    commander = Commander()
    
    # Initialize coder agent
    ollama = OllamaClient()
    coder_agent = CoderAgent(ollama)
    
    # Register agent
    commander.register_agent("coder", coder_agent.execute)
    
    # Execute coding request
    code_request = """
    Generate a Python class that implements a simple binary search tree with:
    1. Insert method
    2. Search method
    3. Delete method
    4. In-order traversal
    
    Include comprehensive docstrings and error handling.
    """
    
    print("\n=== Code Generation Task ===")
    result = await commander.execute(code_request)
    
    print(f"Status: {result.status}")
    print(f"Execution Time: {result.execution_time:.2f}s")
    print("\nGenerated Code:")
    print(result.output)


if __name__ == "__main__":
    asyncio.run(main())
