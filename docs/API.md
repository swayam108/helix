"""API reference documentation"""

# HELIX API Reference

## Commander

Main orchestration engine for HELIX.

### Initialization

```python
from helix.core.commander import Commander

commander = Commander(config={"max_concurrent_agents": 5})
```

### Methods

#### execute(request, context=None)
Execute a task request.

```python
result = await commander.execute(
    "Your task description",
    context={"project": "my_project"}
)
```

**Parameters:**
- `request` (str): Natural language task description
- `context` (dict): Optional execution context

**Returns:** `CommandResult` with output, tasks, and metadata

#### register_agent(agent_type, handler)
Register an agent handler.

```python
commander.register_agent("custom", my_agent.execute)
```

#### get_system_status()
Get current system resource usage.

```python
status = commander.get_system_status()
print(f"CPU: {status['cpu_percent']}%")
```

#### get_execution_history(limit=10)
Get recent execution results.

```python
history = commander.get_execution_history(limit=5)
for result in history:
    print(f"{result.status}: {result.execution_time}s")
```

## Memory

Dual-layer memory system.

### Methods

#### store(key, value, category, importance, ttl_seconds)
Store data in memory.

```python
memory.store(
    "my_key",
    {"data": "value"},
    category="project",
    importance=0.8
)
```

#### retrieve(key)
Retrieve data from memory.

```python
data = memory.retrieve("my_key")
```

#### search(category, limit)
Search memory by category.

```python
results = memory.search("project", limit=10)
```

## EventBus

Inter-agent communication system.

### Methods

#### subscribe(event_type, callback)
Subscribe to event type.

```python
def handler(event):
    print(f"Received: {event.type}")

event_bus.subscribe("task_completed", handler)
```

#### publish(event)
Publish an event.

```python
from helix.core.event_bus import Event

event = Event(
    type="custom_event",
    sender="my_agent",
    data={"key": "value"}
)
await event_bus.publish(event)
```

## BaseAgent

Base class for all agents.

### Methods

#### execute(task)
Execute a task. Must be overridden by subclasses.

```python
async def execute(self, task):
    # Implement task execution
    return result
```

#### validate_task(task)
Validate if agent can execute task.

```python
if agent.validate_task(task):
    result = await agent.run_task(task)
```

#### get_status()
Get agent status.

```python
status = agent.get_status()
print(f"Running tasks: {status['running_tasks']}")
```

## SafetyManager

Permission and security management.

### Methods

#### has_permission(agent, resource, action, constraint)
Check if agent has permission.

```python
if safety.has_permission("coder", "filesystem", "write"):
    # Proceed with operation
    pass
```

#### grant_permission(agent, resource, action, level)
Grant permission to agent.

```python
from helix.utils.safety import PermissionLevel

safety.grant_permission(
    "automation",
    "system",
    "execute",
    PermissionLevel.EXECUTE
)
```

#### get_audit_log(agent, limit)
Get audit log entries.

```python
logs = safety.get_audit_log("coder", limit=100)
```

## OllamaClient

Interface to Ollama LLM.

### Methods

#### generate(prompt, model, temperature, top_k, top_p)
Generate text using LLM.

```python
response = await ollama.generate(
    prompt="Your prompt here",
    model="qwen:32b",
    temperature=0.7
)
```

#### embeddings(text, model)
Generate embeddings for semantic search.

```python
embedding = await ollama.embeddings(
    text="Your text here",
    model="nomic-embed-text"
)
```

#### health_check()
Check if Ollama is running.

```python
if await ollama.health_check():
    print("Ollama is ready")
```

## ToolManager

Manage tools available to agents.

### Methods

#### register_tool(name, description, func, required_permissions)
Register a custom tool.

```python
def my_tool(param1, param2):
    return f"Result: {param1} {param2}"

tool_manager.register_tool(
    name="my_tool",
    description="My custom tool",
    func=my_tool,
    required_permissions=["custom.read"]
)
```

#### execute_tool(tool_name, **kwargs)
Execute a registered tool.

```python
result = tool_manager.execute_tool("my_tool", param1="a", param2="b")
```

#### list_tools()
List all available tools.

```python
tools = tool_manager.list_tools()
for name, tool in tools.items():
    print(f"{name}: {tool.description}")
```

## Data Models

### Task

```python
from helix.models.task import ExecutionTask, TaskStatus, TaskPriority

task = ExecutionTask(
    id="TASK_001",
    description="Do something",
    agent_type="coder",
    priority=TaskPriority.HIGH,
    dependencies=[]
)
```

### CommandResult

```python
result.status  # "pending", "running", "completed", "failed"
result.output  # Task output
result.tasks  # List of executed tasks
result.task_results  # Dict of task outputs
result.execution_time  # Total execution time in seconds
result.errors  # List of error messages
```

## Configuration

### system_config.yaml

```yaml
system:
  max_concurrent_agents: 5
  memory_backend: chroma
  
ollama:
  base_url: http://localhost:11434
  default_model: qwen:32b
  timeout_seconds: 300
```

## Error Handling

```python
try:
    result = await commander.execute("task")
except Exception as e:
    print(f"Execution failed: {e}")
    # Handle error
```

## Async Patterns

```python
import asyncio

async def main():
    commander = Commander()
    result = await commander.execute("Your task")
    return result

result = asyncio.run(main())
```

## Best Practices

1. **Always await async calls**: Use `await` for async functions
2. **Check permissions**: Verify agent permissions before execution
3. **Monitor resources**: Check system status regularly
4. **Handle errors**: Implement proper error handling
5. **Use appropriate models**: Select models based on task type
6. **Cache results**: Store results in memory for future use
7. **Log activities**: Enable audit logging for debugging
