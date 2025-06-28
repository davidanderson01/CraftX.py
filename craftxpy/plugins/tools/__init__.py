"""Auto-discovery system for CraftX.py tool plugins."""

import os
import importlib
from typing import Dict, Any
from .base_tool import BaseTool


def load_tools() -> Dict[str, BaseTool]:
    """Automatically discover and load all tool plugins.

    Returns:
        Dictionary mapping tool names to tool instances
    """
    tools = {}
    tools_dir = os.path.dirname(__file__)

    # Scan all Python files in the tools directory
    for filename in os.listdir(tools_dir):
        if filename.endswith(".py") and filename not in ["__init__.py", "base_tool.py"]:
            module_name = filename[:-3]  # Remove .py extension

            try:
                # Import the module
                module = importlib.import_module(
                    f"craftxpy.plugins.tools.{module_name}")

                # Find all classes that inherit from BaseTool
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)

                    # Check if it's a class and inherits from BaseTool
                    if (isinstance(attr, type) and
                        issubclass(attr, BaseTool) and
                            attr is not BaseTool):

                        try:
                            # Instantiate the tool
                            tool_instance = attr()
                            tools[attr_name] = tool_instance
                        except (TypeError, AttributeError) as e:
                            print(
                                f"⚠️ Failed to instantiate tool {attr_name}: {e}")

            except ImportError as e:
                print(f"⚠️ Failed to import tool module {module_name}: {e}")
            except (AttributeError, TypeError) as e:
                print(f"⚠️ Error loading tools from {module_name}: {e}")

    return tools


def get_tool_info(tools: Dict[str, BaseTool]) -> Dict[str, Dict[str, Any]]:
    """Get information about all loaded tools.

    Args:
        tools: Dictionary of loaded tools

    Returns:
        Dictionary mapping tool names to their metadata
    """
    return {name: tool.get_tool_info() for name, tool in tools.items()}


def list_available_tools() -> Dict[str, BaseTool]:
    """List all available tools with their instances.

    Returns:
        Dictionary of available tools
    """
    return load_tools()


# Load tools on module import
_cached_tools = None


def get_tools() -> Dict[str, BaseTool]:
    """Get cached tools or load them if not cached.

    Returns:
        Dictionary of tool instances
    """
    global _cached_tools  # pylint: disable=global-statement
    if _cached_tools is None:
        _cached_tools = load_tools()
    return _cached_tools


def reload_tools() -> Dict[str, BaseTool]:
    """Force reload all tools (useful for development).

    Returns:
        Dictionary of reloaded tool instances
    """
    global _cached_tools  # pylint: disable=global-statement
    _cached_tools = load_tools()
    return _cached_tools
