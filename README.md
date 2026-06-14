# HELIX: Local-First Multi-Agent AI Operating System

A sophisticated, modular AI swarm where specialized agents think and work together in real-time to solve complex problems, powered entirely by local Ollama models.

## 🎯 Vision

HELIX transforms AI from a single chatbot into a **coordinated AI organization**. Users describe goals in natural language, and a system of specialized agents automatically:

- Break down tasks into sub-tasks
- Distribute work across specialists
- Execute collaboratively with reasoning loops
- Verify and validate results
- Learn from interactions
- Operate entirely offline using Ollama

## 🏗️ Architecture

```
User Intent
    ↓
Commander Agent (understands & routes)
    ↓
Planner Agent (decomposes tasks)
    ↓
Specialist Agents (parallel execution)
    ├─ Research Agent
    ├─ Coder Agent
    ├─ Automation Agent
    ├─ Browser Agent
    ├─ Vision Agent
    └─ [Custom Agents]
    ↓
Validator Agent (verification & quality)
    ↓
Output & Memory System
```

## 🤖 Core Agents

| Agent | Purpose | Powered By |
|-------|---------|----------|
| **Commander** | Intent understanding, system orchestration, flow management | Qwen/Llama 3.1 |
| **Planner** | Task decomposition, step sequencing, dependency analysis | Qwen |
| **Research** | Information gathering, summarization, knowledge synthesis | Llama 3.1 |
| **Coder** | Code generation, debugging, optimization, testing | DeepSeek-Coder / Qwen-Coder |
| **Automation** | System commands, file operations, workflow execution | DeepSeek-R1 |
| **Browser** | Web interaction, data extraction, screenshot analysis | Vision + Research |
| **Vision** | Image recognition, screen analysis, OCR | Llava / Similar |
| **Voice** | Speech-to-text, text-to-speech, acoustic analysis | Local STT/TTS |
| **Memory** | Context storage, semantic search, knowledge retrieval | Vector DB + Search |
| **Security** | Permission management, safe execution, audit logging | Custom Logic |
| **Learning** | Knowledge structuring, pattern extraction, improvement | Ollama + Vector DB |

## 🌟 Key Features

### Multi-Agent Collaboration
- Real-time agent communication
- Shared context and memory
- Peer review and validation
- Parallel task execution
- Dynamic agent spawning/destruction

### Task Management
- Intelligent task decomposition
- Dependency resolution
- Priority queuing
- Timeout handling
- Rollback on failure

### Memory System
- **Short-term**: Active task context (vector embeddings)
- **Long-term**: User preferences, project history, learned patterns
- **Semantic search**: Find relevant knowledge across stored context

### Resource Control
- CPU/GPU/RAM/VRAM monitoring
- Auto-scaling of active agents
- Task complexity budgeting
- Graceful degradation under load

### Safety & Security
- Permission-based execution
- Sandbox isolation for untrusted tasks
- Audit logging of all actions
- User consent for file/system operations

### Ollama Model Routing
```
Task Type → Model Selection
├─ General reasoning → Qwen 32B / Llama 3.1 70B
├─ Code generation → DeepSeek-Coder 33B / Qwen-Coder
├─ Complex reasoning → DeepSeek-R1 32B
├─ Fast response → Phi 3.5 / Mistral
└─ Specialized (Vision, etc.) → Llava / Specialized models
```

## 📦 Project Structure

```
helix/
├── README.md
├── requirements.txt
├── setup.py
├── LICENSE
├── .gitignore
│
├── config/
│   ├── agents.yaml          # Agent definitions & capabilities
│   ├── models.yaml          # Model configurations & routing rules
│   ├── system_config.yaml   # System-wide settings
│   └── prompts/             # Agent prompts & instructions
│
├── core/
│   ├── __init__.py
│   ├── commander.py         # Main orchestrator
│   ├── planner.py           # Task decomposition
│   ├── executor.py          # Task execution engine
│   ├── memory.py            # Memory & context management
│   ├── event_bus.py         # Agent communication
│   └── resource_monitor.py  # System resource tracking
│
├── agents/
│   ├── __init__.py
│   ├── base.py              # Base agent class
│   ├── commander_agent.py
│   ├── planner_agent.py
│   ├── research_agent.py
│   ├── coder_agent.py
│   ├── automation_agent.py
│   ├── browser_agent.py
│   ├── vision_agent.py
│   ├── voice_agent.py
│   ├── memory_agent.py
│   ├── security_agent.py
│   └── learning_agent.py
│
├── tools/
│   ├── __init__.py
│   ├── file_operations.py   # File I/O tools
│   ├── system_commands.py   # Shell execution (safe)
│   ├── browser_tools.py     # Web scraping, automation
│   ├── code_tools.py        # Code execution, linting
│   └── custom_tools.py      # User-defined tools
│
├── models/
│   ├── task.py              # Task data structures
│   ├── agent.py             # Agent definitions
│   ├── message.py           # Message/communication formats
│   ├── memory.py            # Memory entry models
│   └── resource.py          # Resource monitoring models
│
├── utils/
│   ├── logger.py            # Structured logging
│   ├── ollama_client.py     # Ollama API wrapper
│   ├── vector_db.py         # Semantic search (Chroma/Milvus)
│   ├── safety.py            # Safety checks and validation
│   └── helpers.py           # Utility functions
│
├── ui/
│   ├── __init__.py
│   ├── web_interface.py     # Web dashboard (Flask/FastAPI)
│   ├── cli_interface.py     # CLI interface
│   ├── voice_interface.py   # Voice input/output
│   └── visualizations/      # 3D visualization (Three.js/Babylon)
│
├── plugins/
│   ├── __init__.py
│   └── registry.py          # Plugin system
│
├── tests/
│   ├── test_agents.py
│   ├── test_tasks.py
│   ├── test_memory.py
│   └── test_integration.py
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── AGENT_DEVELOPMENT.md
│   ├── MEMORY.md
│   ├── SECURITY.md
│   ├── API.md
│   └── EXAMPLES.md
│
└── examples/
    ├── basic_usage.py
    ├── code_generation.py
    ├── research_task.py
    └── complex_workflow.py
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Ollama installed and running (`ollama serve`)
- 16GB+ RAM (32GB recommended for multiple models)
- GPU support optional but recommended

### Installation

```bash
# Clone the repository
git clone https://github.com/swayam108/HELIX.git
cd HELIX

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull required Ollama models
ollama pull llama2
ollama pull qwen:32b
ollama pull deepseek-coder:33b
ollama pull mistral

# Start HELIX
python -m helix.cli
```

### Example Usage

```python
from helix import HELIX

# Initialize the system
helix = HELIX()

# Simple request
result = helix.execute("Write a Python function to solve the traveling salesman problem")

# Complex workflow
result = helix.execute("""
    Research the latest advances in quantum computing,
    summarize key findings,
    and write a blog post explaining them to beginners
""")

# Access results
print(result.output)
print(result.agents_used)
print(result.execution_time)
```

## 🔄 Execution Flow

1. **User Input** → Natural language request via CLI/Web/Voice
2. **Commander** → Parses intent, routes to appropriate agents
3. **Planner** → Decomposes into actionable tasks with dependencies
4. **Parallel Execution** → Agents work on tasks concurrently
5. **Inter-Agent Communication** → Agents share context via event bus
6. **Validation** → Results verified for quality and accuracy
7. **Learning** → Interactions stored for future optimization
8. **Output** → Synthesized results delivered to user
9. **Memory Update** → Context stored for long-term learning

## 🧠 Memory System

### Short-Term Memory
- Current conversation context
- Active task state
- Agent outputs and intermediate results
- Token-efficient retrieval

### Long-Term Memory
- User preferences and goals
- Project history and completed tasks
- Learned patterns and optimizations
- Semantic search via embeddings

```python
# Example: Memory operations
memory = helix.memory

# Store
memory.store_interaction({
    "user_request": "...",
    "decomposition": [...],
    "results": {...},
    "execution_time": 45.2
})

# Retrieve
similar_tasks = memory.semantic_search("similar web scraping task", top_k=3)
context = memory.get_user_context()
```

## ⚙️ Configuration

Edit `config/system_config.yaml`:

```yaml
system:
  max_concurrent_agents: 5
  memory_backend: "chroma"  # or milvus, pinecone
  
ollama:
  base_url: "http://localhost:11434"
  default_model: "qwen:32b"
  timeout: 300
  
agents:
  enabled:
    - commander
    - planner
    - research
    - coder
    - automation
    
safety:
  enable_sandboxing: true
  require_confirmation: true
  audit_logging: true
```

## 🛡️ Safety & Permissions

All agents operate within a permission framework:

```python
# Agents declare required permissions
@agent
class FileOperationAgent(BaseAgent):
    required_permissions = [
        "filesystem.read",
        "filesystem.write",
        "filesystem.execute"
    ]
```

Users grant/deny permissions:

```python
helix.security.request_permission(
    agent="automation",
    action="execute_shell_command",
    resource="/home/user/scripts/setup.sh"
)
```

## 📊 Monitoring & Logging

Real-time monitoring of system state:

```python
# Monitor resource usage
status = helix.get_system_status()
print(f"Active agents: {status.active_agents}")
print(f"CPU: {status.cpu_percent}%")
print(f"Memory: {status.memory_percent}%")
print(f"GPU: {status.gpu_memory_used}GB")

# View execution logs
logs = helix.get_execution_logs(task_id="xyz")
for log in logs:
    print(f"[{log.timestamp}] {log.agent}: {log.message}")
```

## 🧩 Plugin System

Extend HELIX with custom agents and tools:

```python
# Custom agent
from helix.agents.base import BaseAgent

class DataAnalysisAgent(BaseAgent):
    name = "data_analyst"
    description = "Analyzes datasets and generates insights"
    
    async def execute(self, task):
        # Implementation
        pass

# Register
helix.plugin_registry.register_agent(DataAnalysisAgent())

# Custom tool
@helix.register_tool
def analyze_csv(filepath: str) -> dict:
    """Analyze CSV file and return statistics"""
    pass
```

## 🎨 3D Visualization Interface

HELIX includes a real-time 3D visualization showing:
- Agent nodes and connections
- Active task flows
- Resource utilization
- Communication channels

Access at `http://localhost:8000/visualize`

## 📚 Documentation

- [Architecture Deep Dive](docs/ARCHITECTURE.md)
- [Agent Development Guide](docs/AGENT_DEVELOPMENT.md)
- [Memory System Documentation](docs/MEMORY.md)
- [Safety & Security](docs/SECURITY.md)
- [API Reference](docs/API.md)
- [Examples & Tutorials](docs/EXAMPLES.md)

## 🔬 Research & Innovation

HELIX is designed to support research in:
- Multi-agent coordination
- Emergent behavior in AI systems
- Efficient resource allocation
- Knowledge synthesis and learning
- Decentralized task execution

## 🤝 Contributing

We welcome contributions:
1. Fork the repository
2. Create a feature branch
3. Submit pull requests with tests
4. Follow our [Contributing Guide](CONTRIBUTING.md)

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 🎓 Learning Resources

- [Getting Started Guide](docs/GETTING_STARTED.md)
- [Agent Communication Protocol](docs/PROTOCOL.md)
- [Task Definition Format](docs/TASK_FORMAT.md)

## 🚨 Known Limitations & Roadmap

### Current Phase
- ✅ Core agent framework
- ✅ Basic task decomposition
- ✅ Memory system foundation
- 🔄 Multi-agent coordination
- 🔄 Advanced tool integration

### Upcoming
- [ ] Distributed execution (multiple machines)
- [ ] Advanced reasoning with chain-of-thought
- [ ] Automatic curriculum learning
- [ ] Real-time collaboration UI
- [ ] Advanced Ollama model optimization
- [ ] Hardware acceleration (CUDA/ROCm tuning)

## ⚡ Performance Targets

- Task decomposition: < 2s
- Inter-agent communication: < 100ms
- Memory semantic search: < 500ms
- Average task completion: task-dependent
- Concurrent agents: 5-10 depending on hardware

## 📞 Support & Community

- [Discussions](https://github.com/swayam108/HELIX/discussions)
- [Issues](https://github.com/swayam108/HELIX/issues)

---

**HELIX: Where Local AI Becomes Intelligent Organization** 🧬
