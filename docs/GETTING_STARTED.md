"""Getting started guide"""

# Getting Started with HELIX

## Installation

### Prerequisites
- Python 3.11 or higher
- Ollama installed and running
- 16GB+ RAM (32GB recommended)
- Optional: GPU with CUDA support

### Step 1: Install Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai)

```bash
# Verify Ollama installation
ollama --version

# Start Ollama server
ollama serve
```

### Step 2: Clone and Setup HELIX

```bash
git clone https://github.com/swayam108/HELIX.git
cd HELIX

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Pull Models

```bash
# Download required models (first time only)
ollama pull qwen:32b
ollama pull deepseek-coder:33b
ollama pull llama2:latest
ollama pull mistral:latest

# Optional: Additional models
ollama pull deepseek-r1:32b
ollama pull phi:latest
```

### Step 4: Verify Installation

```bash
# Test HELIX
python -m helix.cli status
```

## Quick Start

### Command Line Usage

```bash
# Simple execution
python -m helix.cli execute "Write a Python function for binary search"

# Check system status
python -m helix.cli status

# View execution history
python -m helix.cli history --limit 10

# Interactive mode
python -m helix.cli interactive
```

### Python API

```python
from helix.core.commander import Commander
import asyncio

async def main():
    commander = Commander()
    result = await commander.execute("Your task here")
    print(result.output)

asyncio.run(main())
```

## Configuration

Edit `config/system_config.yaml` to customize HELIX:

```yaml
system:
  max_concurrent_agents: 5
  memory_backend: chroma

ollama:
  base_url: http://localhost:11434
  default_model: qwen:32b
```

## Examples

### 1. Simple Task

```bash
python examples/basic_usage.py
```

### 2. Complex Workflow

```bash
python examples/complex_workflow.py
```

### 3. Research Task

```bash
python examples/research_task.py
```

### 4. Code Generation

```bash
python examples/code_generation.py
```

## Troubleshooting

### Ollama Connection Error

```
Error: Cannot connect to Ollama
```

**Solution**: Ensure Ollama is running
```bash
ollama serve
```

### Model Not Found

```
Error: Model not found: qwen:32b
```

**Solution**: Pull the model
```bash
ollama pull qwen:32b
```

### Memory Error

```
Error: Out of memory
```

**Solution**: Reduce concurrent agents or use smaller models
```yaml
system:
  max_concurrent_agents: 2
```

## Next Steps

1. Read the [Architecture Documentation](ARCHITECTURE.md)
2. Explore [Examples](../examples/)
3. Create your own [Custom Agents](AGENT_DEVELOPMENT.md)
4. Check out [API Reference](API.md)
5. Join our community discussions

## Support

- **Documentation**: See `docs/` directory
- **Issues**: Report bugs on GitHub
- **Discussions**: Ask questions in Discussions
- **Examples**: Check `examples/` directory

## Performance Tips

1. **Use appropriate models** for each task
2. **Enable GPU acceleration** if available
3. **Monitor resource usage** with `status` command
4. **Batch related tasks** together
5. **Tune max_concurrent_agents** based on hardware

## Security Considerations

- Always run HELIX in a trusted environment
- Review agent permissions before granting access
- Monitor audit logs for suspicious activity
- Use sandboxing for untrusted code execution
- Keep Ollama and dependencies updated
