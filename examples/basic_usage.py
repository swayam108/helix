"""Basic usage example for HELIX"""

import asyncio
from helix.core.commander import Commander


async def main():
    """Run basic example"""
    # Initialize HELIX
    commander = Commander()
    
    # Example 1: Simple task
    print("\n=== Example 1: Simple Code Generation ===")
    result = await commander.execute(
        "Write a Python function that calculates the factorial of a number"
    )
    print(f"Status: {result.status}")
    print(f"Execution time: {result.execution_time:.2f}s")
    print(f"Output: {result.output}")
    
    # Example 2: Check system status
    print("\n=== System Status ===")
    status = commander.get_system_status()
    for key, value in status.items():
        print(f"{key}: {value}")
    
    # Example 3: View execution history
    print("\n=== Execution History ===")
    history = commander.get_execution_history(limit=5)
    for i, result in enumerate(history, 1):
        print(f"{i}. {result.status} - {result.execution_time:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
