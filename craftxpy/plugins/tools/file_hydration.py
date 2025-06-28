"""File hydration monitoring tool for CraftX.py (Windows OneDrive)."""

import os
from .base_tool import BaseTool


class FileHydrationMonitor(BaseTool):
    """Tool for monitoring file hydration status on Windows (OneDrive)."""

    def __init__(self):
        super().__init__()
        self.description = "Monitor file hydration status for OneDrive files on Windows"
        self.version = "1.0.0"
        self.parameters = {
            "path": {
                "type": "string",
                "description": "File or directory path to check",
                "required": True
            }
        }

    def run(self, path: str = None, **kwargs) -> str:
        """Check file hydration status.

        Args:
            path: The file or directory path to check
            **kwargs: Additional parameters (ignored)

        Returns:
            File hydration status result
        """
        if not path:
            return "❌ Path parameter is required"

        if not path.strip():
            return "❌ Path cannot be empty"

        clean_path = path.strip()

        if not os.path.exists(clean_path):
            return f"❌ Path not found: {clean_path}"

        try:
            # Check if it's a file or directory
            if os.path.isfile(clean_path):
                return self._check_file_hydration(clean_path)
            elif os.path.isdir(clean_path):
                return self._check_directory_hydration(clean_path)
            else:
                return f"❓ Unknown path type: {clean_path}"

        except (OSError, PermissionError) as e:
            return f"❌ Error checking {clean_path}: {str(e)}"

    def _check_file_hydration(self, file_path: str) -> str:
        """Check hydration status of a single file."""
        try:
            # On Windows, check file attributes for OneDrive dehydration
            file_stat = os.stat(file_path)

            # FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS = 0x400000
            # This indicates the file is not fully hydrated
            if hasattr(file_stat, 'st_file_attributes'):
                attributes = file_stat.st_file_attributes
                if attributes & 0x400000:  # Not hydrated
                    return f"⚠️ {file_path} - Not fully hydrated (OneDrive placeholder)"
                else:
                    return f"✅ {file_path} - Fully hydrated"
            else:
                # Fallback: check file size and accessibility
                size = file_stat.st_size
                if size == 0:
                    return f"⚠️ {file_path} - Possibly not hydrated (0 bytes)"
                else:
                    return f"✅ {file_path} - Appears hydrated ({size} bytes)"

        except OSError as e:
            return f"❌ Cannot access {file_path}: {str(e)}"

    def _check_directory_hydration(self, dir_path: str) -> str:
        """Check hydration status of files in a directory."""
        try:
            file_count = 0
            hydrated_count = 0

            for root, _, files in os.walk(dir_path):
                for file in files[:10]:  # Limit to first 10 files to avoid spam
                    file_path = os.path.join(root, file)
                    file_count += 1

                    try:
                        file_stat = os.stat(file_path)
                        if hasattr(file_stat, 'st_file_attributes'):
                            attributes = file_stat.st_file_attributes
                            if not (attributes & 0x400000):  # Is hydrated
                                hydrated_count += 1
                        else:
                            if file_stat.st_size > 0:
                                hydrated_count += 1
                    except OSError:
                        continue

                # Only check first level to avoid deep recursion
                break

            if file_count == 0:
                return f"📁 {dir_path} - No files found"

            percentage = (hydrated_count / file_count) * 100
            status = "✅" if percentage > 80 else "⚠️" if percentage > 50 else "❌"

            return f"{status} {dir_path} - {hydrated_count}/{file_count} files hydrated ({percentage:.1f}%)"

        except OSError as e:
            return f"❌ Cannot access directory {dir_path}: {str(e)}"
