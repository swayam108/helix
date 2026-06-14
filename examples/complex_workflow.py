"""Complex workflow example"""

import asyncio
from helix.core.commander import Commander


async def main():
    """Run complex workflow example"""
    commander = Commander()
    
    # Multi-step workflow: Research + Code + Automation
    complex_request = """
    1. Research the latest advancements in machine learning for 2024
    2. Write a Python script that demonstrates a key concept from your research
    3. Create a documentation file explaining the concept and the code
    """
    
    print("\n=== Complex Workflow Execution ===")
    print(f"Request: {complex_request}")
    print("\nProcessing...\n")
    
    result = await commander.execute(complex_request)
    
    print(f"Status: {result.status}")
    print(f"Execution Time: {result.execution_time:.2f}s")
    print(f"Tasks Executed: {len(result.tasks)}")
    print("\nTask Details:")
    for task in result.tasks:
        print(f"  - {task.id}: {task.description} (Agent: {task.agent_type})")
    
    print("\nOutput:")
    print(result.output)
    
    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  - {error}")


if __name__ == "__main__":
    asyncio.run(main())
