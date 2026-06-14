"""Plugin system for extensibility"""

from typing import Dict, Type, Callable, Any
from abc import ABC, abstractmethod
from helix.utils.logger import get_logger

logger = get_logger(__name__)


class Plugin(ABC):
    """Base class for HELIX plugins"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name"""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version"""
        pass

    @abstractmethod
    async def initialize(self, context: Dict[str, Any]) -> None:
        """Initialize the plugin"""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up plugin resources"""
        pass


class PluginRegistry:
    """Registry for HELIX plugins"""

    def __init__(self):
        self.agents: Dict[str, Type] = {}
        self.tools: Dict[str, Callable] = {}
        self.plugins: Dict[str, Plugin] = {}

    def register_agent(self, agent_class: Type, agent_type: str = None) -> None:
        """Register a custom agent"""
        agent_type = agent_type or agent_class.__name__.lower()
        self.agents[agent_type] = agent_class
        logger.info(f"Registered custom agent: {agent_type}")

    def register_tool(self, tool_name: str, tool_func: Callable) -> None:
        """Register a custom tool"""
        self.tools[tool_name] = tool_func
        logger.info(f"Registered custom tool: {tool_name}")

    def register_plugin(self, plugin: Plugin) -> None:
        """Register a plugin"""
        self.plugins[plugin.name] = plugin
        logger.info(f"Registered plugin: {plugin.name} v{plugin.version}")

    def get_agent(self, agent_type: str) -> Type:
        """Get a registered agent class"""
        return self.agents.get(agent_type)

    def get_tool(self, tool_name: str) -> Callable:
        """Get a registered tool"""
        return self.tools.get(tool_name)

    def get_plugin(self, plugin_name: str) -> Plugin:
        """Get a registered plugin"""
        return self.plugins.get(plugin_name)

    def list_agents(self) -> Dict[str, Type]:
        """List all registered agents"""
        return self.agents.copy()

    def list_tools(self) -> Dict[str, Callable]:
        """List all registered tools"""
        return self.tools.copy()

    def list_plugins(self) -> Dict[str, Plugin]:
        """List all registered plugins"""
        return self.plugins.copy()
