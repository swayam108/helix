"""Tool definitions and management"""

from typing import Callable, Dict, Any, Optional
from dataclasses import dataclass
from helix.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Tool:
    """Definition of a tool that agents can use"""
    name: str
    description: str
    func: Callable
    required_permissions: list = None
    input_schema: Dict[str, Any] = None
    output_schema: Dict[str, Any] = None


class ToolManager:
    """Manages available tools for agents"""

    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        """Register default tools"""
        # Example: file reading tool
        self.register_tool(
            name="read_file",
            description="Read contents of a file",
            func=self._read_file,
            required_permissions=["filesystem.read"]
        )

    def register_tool(
        self,
        name: str,
        description: str,
        func: Callable,
        required_permissions: list = None,
        input_schema: Dict[str, Any] = None,
        output_schema: Dict[str, Any] = None
    ) -> None:
        """Register a new tool"""
        tool = Tool(
            name=name,
            description=description,
            func=func,
            required_permissions=required_permissions or [],
            input_schema=input_schema,
            output_schema=output_schema
        )
        self.tools[name] = tool
        logger.info(f"Registered tool: {name}")

    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools.get(name)

    def list_tools(self) -> Dict[str, Tool]:
        """List all available tools"""
        return self.tools.copy()

    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a tool"""
        tool = self.get_tool(tool_name)
        if not tool:
            raise ValueError(f"Tool not found: {tool_name}")
        
        try:
            return tool.func(**kwargs)
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            raise

    @staticmethod
    def _read_file(filepath: str) -> str:
        """Read file contents"""
        with open(filepath, 'r') as f:
            return f.read()
