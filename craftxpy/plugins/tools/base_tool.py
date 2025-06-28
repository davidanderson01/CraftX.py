"""Base tool interface for CraftX.py tool plugins."""

# Standard library imports
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """Base class for all tool plugins in CraftX.py."""

    def __init__(self):
        self.tool_name = self.__class__.__name__

    @abstractmethod
    def run(self, **kwargs) -> str:
        """Execute the tool with given parameters.

        Args:
            **kwargs: Tool-specific parameters

        Returns:
            Tool execution result as string

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Must implement run() method")

    def get_tool_info(self) -> Dict[str, Any]:
        """Get information about this tool.

        Returns:
            Dictionary containing tool metadata
        """
        return {
            "name": self.tool_name,
            "description": getattr(self, "description", "No description available"),
            "version": getattr(self, "version", "1.0.0"),
            "parameters": getattr(self, "parameters", {})
        }
