from dataclasses import dataclass
from enum import Enum
from typing import Any
from typing import Callable
from typing import Optional


class ToolCategory(Enum):
    """Enum representing the categories of tools."""

    DESIGN = "design"
    EXCEL = "excel"
    DRIVE = "drive"
    NOTIFICATION = "notification"
    ADMIN = "admin"


@dataclass
class ToolDefinition:
    """Definition of a tool available to the AI agent."""

    name: str
    description: str
    category: ToolCategory
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    handler: Callable
    requires_auth: bool = False
    admin_only: bool = False


class ToolRegistry:
    """Registry of all tools available to the AI agent."""

    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        """Register a new tool."""
        if tool.name in self._tools:
            raise ValueError(f"Tool {tool.name} is already registered")
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        """Get a tool by name."""
        return self._tools.get(name)

    def get_tools_by_category(self, category: ToolCategory) -> list[ToolDefinition]:
        """Get all tools in a specific category."""
        return [tool for tool in self._tools.values() if tool.category == category]

    def get_customer_tools(self) -> list[ToolDefinition]:
        """Get all tools available to customers."""
        return [tool for tool in self._tools.values() if not tool.admin_only]

    def get_admin_tools(self) -> list[ToolDefinition]:
        """Get all tools available to admins."""
        return [tool for tool in self._tools.values() if tool.admin_only]


# Default tool registry instance
default_registry = ToolRegistry()
