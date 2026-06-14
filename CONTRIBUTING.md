"""Contributing guidelines"""

# Contributing to HELIX

We welcome contributions from the community! Here's how to get started.

## Development Setup

```bash
# Clone repository
git clone https://github.com/swayam108/HELIX.git
cd HELIX

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio black flake8 mypy

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

## Code Style

We follow PEP 8 with some customizations:

```bash
# Format code
black helix/

# Check style
flake8 helix/ --max-line-length=100

# Type checking
mypy helix/
```

## Creating Custom Agents

1. Extend `BaseAgent` class
2. Implement `execute()` and `validate_task()` methods
3. Add required permissions
4. Register with commander

```python
from helix.agents.base import BaseAgent
from helix.models.agent import AgentConfig, AgentType

class MyAgent(BaseAgent):
    def __init__(self):
        config = AgentConfig(
            name="My Agent",
            agent_type=AgentType.CUSTOM,
            description="Does something"
        )
        super().__init__(config)
    
    async def execute(self, task):
        # Implement execution logic
        pass
    
    def validate_task(self, task):
        return True
```

## Creating Custom Tools

```python
from helix.tools.tool_manager import ToolManager

tool_manager = ToolManager()

def my_tool(param1: str) -> str:
    """My custom tool"""
    return f"Result: {param1}"

tool_manager.register_tool(
    name="my_tool",
    description="My custom tool",
    func=my_tool,
    required_permissions=["custom.execute"]
)
```

## Testing

Write tests for your contributions:

```python
import pytest

@pytest.mark.asyncio
async def test_my_agent():
    agent = MyAgent()
    task = create_test_task()
    result = await agent.execute(task)
    assert result is not None
```

Run tests:

```bash
pytest tests/ -v
```

## Documentation

Update documentation for new features:

1. Add docstrings to functions/classes
2. Update README if user-facing
3. Add examples in `examples/` directory
4. Update API reference if applicable

## Commit Guidelines

Use conventional commit format:

```
feat: Add new agent type
fix: Resolve memory leak in executor
refactor: Improve event bus performance
docs: Update API documentation
test: Add tests for safety manager
```

## Pull Request Process

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Make changes and commit: `git commit -am 'feat: Add my feature'`
4. Push to branch: `git push origin feature/my-feature`
5. Create Pull Request with description
6. Ensure all checks pass
7. Request review from maintainers

## Code Review

PRs are reviewed for:
- Code quality and style
- Test coverage
- Documentation
- Performance impact
- Security implications

## Reporting Issues

Include:
- Description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)
- Relevant logs or error messages

## Feature Requests

Describe:
- Problem being solved
- Proposed solution
- Alternative approaches
- Potential impact

## Community

- **Discussions**: Ask questions, share ideas
- **Issues**: Report bugs, request features
- **Pull Requests**: Contribute code
- **Documentation**: Help improve docs

## License

By contributing, you agree your contributions are licensed under the MIT License.

## Questions?

Open an issue or start a discussion in the GitHub repository.
