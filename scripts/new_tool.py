"""Tool generator script for CraftX.py."""

import os
import sys
import re

TOOL_TEMPLATE = '''"""{{description}} for CraftX.py."""

from .base_tool import BaseTool

class {{class_name}}(BaseTool):
    """{{description}} implementation."""

    def __init__(self):
        super().__init__()
        self.description = "{{description}}"
        self.version = "1.0.0"
        self.parameters = {
            # Define tool parameters here
            # Example:
            # "input_text": {
            #     "type": "string",
            #     "description": "Input text to process",
            #     "required": True
            # }
        }

    def run(self, **kwargs) -> str:
        """Execute the {{description}}.

        Args:
            **kwargs: Tool-specific parameters

        Returns:
            Tool execution result
        """
        # TODO: Implement your tool logic here
        return "✅ {{class_name}} executed successfully."
'''


def create_tool(name: str, description: str = None) -> str:
    """Create a new tool plugin.

    Args:
        name: The tool name (e.g., "PDF Converter")
        description: Optional description (defaults to name)

    Returns:
        Success message with file path
    """
    if not name.strip():
        return "❌ Tool name cannot be empty"

    # Generate class name (PascalCase) - remove special characters
    class_name = "".join(word.capitalize()
                         for word in name.replace("-", " ").split() if word.isalnum())

    # Ensure class name is valid
    if not class_name:
        return "❌ Tool name must contain at least one alphanumeric word"

    # Ensure class name doesn't start with a number
    if class_name[0].isdigit():
        class_name = "Tool" + class_name

    # Generate filename (snake_case) - sanitize for filesystem
    # Remove special chars except spaces and hyphens
    filename = re.sub(r'[^\w\s-]', '', name.lower())
    # Replace spaces and hyphens with underscores
    filename = re.sub(r'[-\s]+', '_', filename)
    # Remove leading/trailing underscores
    filename = filename.strip('_') + ".py"

    # Ensure filename is valid
    if filename == ".py" or filename.startswith("_.py"):
        return "❌ Tool name must contain valid characters for filename"

    # Use name as description if not provided
    if not description:
        description = name

    # Generate file path
    tools_dir = os.path.join("craftxpy", "plugins", "tools")
    if not os.path.exists(tools_dir):
        return f"❌ Tools directory not found: {tools_dir}"

    file_path = os.path.join(tools_dir, filename)

    # Check if file already exists
    if os.path.exists(file_path):
        return f"❌ Tool file already exists: {file_path}"

    # Generate tool code
    tool_code = TOOL_TEMPLATE.replace("{{class_name}}", class_name)
    tool_code = tool_code.replace("{{description}}", description)

    try:
        # Write the tool file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(tool_code)

        return f"✅ Created tool: {file_path}\n" \
            f"   Class: {class_name}\n" \
            f"   Description: {description}\n" \
            f"\n💡 Don't forget to implement the run() method!"

    except IOError as e:
        return f"❌ Failed to create tool file: {str(e)}"


def list_existing_tools() -> str:
    """List all existing tools.

    Returns:
        List of existing tools
    """
    tools_dir = os.path.join("craftxpy", "plugins", "tools")

    if not os.path.exists(tools_dir):
        return "❌ Tools directory not found"

    tools = []
    for filename in os.listdir(tools_dir):
        if filename.endswith(".py") and filename not in ["__init__.py", "base_tool.py"]:
            tool_name = filename[:-3].replace("_", " ").title()
            tools.append(f"  📦 {tool_name} ({filename})")

    if not tools:
        return "📭 No custom tools found"

    return "🔧 Existing Tools:\n" + "\n".join(tools)


def main():
    """Main tool generator interface."""
    print("🛠️ CraftX.py Tool Generator")
    print("=" * 40)

    if len(sys.argv) > 1:
        # Command line usage
        if sys.argv[1] == "list":
            print(list_existing_tools())
            return

        tool_name = " ".join(sys.argv[1:])
        description = None

        # Check if description is provided with --desc flag
        if "--desc" in sys.argv:
            desc_index = sys.argv.index("--desc")
            if desc_index + 1 < len(sys.argv):
                description = sys.argv[desc_index + 1]
                # Remove --desc and description from tool name
                tool_name = " ".join([arg for i, arg in enumerate(sys.argv[1:], 1)
                                      if i != desc_index and i != desc_index + 1])
            else:
                print("❌ --desc flag requires a description argument")
                return

        if not tool_name.strip():
            print("❌ Tool name cannot be empty")
            return
    else:
        # Interactive usage
        print("\nOptions:")
        print("1. Create new tool")
        print("2. List existing tools")

        choice = input("\nEnter choice (1-2): ").strip()

        if choice == "2":
            print(list_existing_tools())
            return
        elif choice != "1":
            print("❌ Invalid choice")
            return

        tool_name = input("Enter tool name (e.g., 'PDF Converter'): ").strip()
        description = input(
            "Enter description (optional, press Enter to skip): ").strip()

        if not description:
            description = None

    # Create the tool
    result = create_tool(tool_name, description)
    print(f"\n{result}")


if __name__ == "__main__":
    main()
