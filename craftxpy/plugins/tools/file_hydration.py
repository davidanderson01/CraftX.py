"""File hydration monitoring tool for CraftX.py (Windows OneDrive)."""

import os
from .base_tool import BaseTool
from .large_storage_manager import LargeStorageManager


class FileHydrationMonitor(BaseTool):
    """Tool for monitoring file hydration status for OneDrive files on Windows."""

    def __init__(self):
        super().__init__()
        self.description = (
            "Monitor file hydration status for OneDrive files on Windows. "
            "Supports large-scale storage analysis."
        )
        self.version = "2.0.0"
        self.parameters = {
            "path": {
                "type": "string",
                "description": "File or directory path to check",
                "required": True
            },
            "max_files": {
                "type": "integer",
                "description": (
                    "Maximum number of files to check "
                    "(default: 100, use 1000+ for large scans)"
                ),
                "required": False,
                "default": 100
            },
            "deep_scan": {
                "type": "boolean",
                "description": "Perform deep recursive scan for complete analysis",
                "required": False,
                "default": False
            },
            "large_scale": {
                "type": "boolean",
                "description": (
                    "Use large-scale scanning for 1TB+ storage volumes"
                ),
                "required": False,
                "default": False
            }
        }

    def run(self, path: str = None, max_files: int = 100, deep_scan: bool = False,
            large_scale: bool = False, **kwargs) -> str:
        """Check file hydration status.

        Args:
            path: The file or directory path to check
            max_files: Maximum number of files to check per directory
            deep_scan: Whether to perform deep recursive scan
            large_scale: Whether to use large-scale scanning for volumes larger than 1 TB
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
            if os.path.isdir(clean_path):
                if large_scale:
                    return self.run_large_scale_scan(clean_path, max_files, deep_scan)
                return self._check_directory_hydration(clean_path, max_files, deep_scan)

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
                    return (
                        f"⚠️ {file_path} - Not fully hydrated (OneDrive placeholder)"
                    )
                return f"✅ {file_path} - Fully hydrated"
            # Fallback: check file size and accessibility
            size = file_stat.st_size
            if size == 0:
                return f"⚠️ {file_path} - Possibly not hydrated (0 bytes)"

            return f"✅ {file_path} - Appears hydrated ({size} bytes)"

        except OSError as e:
            return f"❌ Cannot access {file_path}: {str(e)}"

    def _check_directory_hydration(self, dir_path: str, max_files: int = 100,
                                   deep_scan: bool = False) -> str:
        """Check hydration status of files in a directory.

        Args:
            dir_path: Directory path to check
            max_files: Maximum number of files to check (default 100)
            deep_scan: Whether to perform deep recursive scan
        """
        try:
            file_count = 0
            hydrated_count = 0
            total_size = 0
            hydrated_size = 0
            directories_scanned = 0

            for root, dirs, files in os.walk(dir_path):
                directories_scanned += 1

                # For large directories, sample files instead of checking all
                if len(files) > max_files:
                    # Sample files evenly across the directory
                    step = len(files) // max_files
                    files = files[::step][:max_files]

                for file in files:
                    if file_count >= max_files and not deep_scan:
                        break

                    file_path = os.path.join(root, file)
                    file_count += 1

                    try:
                        file_stat = os.stat(file_path)
                        file_size = file_stat.st_size
                        total_size += file_size

                        is_hydrated = True
                        if hasattr(file_stat, 'st_file_attributes'):
                            attributes = file_stat.st_file_attributes
                            # Not a placeholder
                            is_hydrated = not attributes & 0x400000
                        else:
                            is_hydrated = file_size > 0

                        if is_hydrated:
                            hydrated_count += 1
                            hydrated_size += file_size

                    except OSError:
                        continue

                # Control recursion depth for performance
                if not deep_scan and directories_scanned >= 10:
                    dirs.clear()  # Don't recurse further
                    break

            if file_count == 0:
                return f"📁 {dir_path} - No files found"

            percentage = (hydrated_count / file_count) * 100
            size_percentage = (
                (hydrated_size / total_size * 100) if total_size > 0 else 0
            )

            status = "✅" if percentage > 80 else "⚠️" if percentage > 50 else "❌"

            # Format sizes
            total_size_str = self._format_size(total_size)
            hydrated_size_str = self._format_size(hydrated_size)

            result = (
                f"{status} {dir_path} - {hydrated_count}/{file_count} files "
                f"hydrated ({percentage:.1f}%)"
            )
            result += (
                f"\n  📊 Size: {hydrated_size_str}/{total_size_str} "
                f"hydrated ({size_percentage:.1f}%)"
            )

            if directories_scanned > 1:
                result += f"\n  📂 Scanned {directories_scanned} directories"

            if file_count >= max_files and not deep_scan:
                result += (
                    f"\n  ⚠️ Limited to {max_files} files. "
                    "Use deep_scan=True for complete analysis"
                )

            return result

        except OSError as e:
            return f"❌ Cannot access directory {dir_path}: {str(e)}"

    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def run_large_scale_scan(self, path: str, max_files: int = 1000,
                             deep_scan: bool = False) -> str:
        """Run a large-scale hydration scan optimized for big directories.

        Args:
            path: Directory path to scan
            max_files: Maximum number of files to process (optional)
            deep_scan: Whether to perform deep analysis (optional)

        Returns:
            Formatted scan results as string
        """
        if not os.path.exists(path):
            return f"❌ Path not found: {path}"

        if not os.path.isdir(path):
            return self._check_file_hydration(path)

        # Import large storage manager for advanced scanning
        manager = LargeStorageManager()

        # Quick scan for immediate results
        result = [f"� Large-scale hydration scan for: {path}"]
        result.append("=" * 50)

        total_files = 0
        total_size = 0
        hydrated_files = 0
        hydrated_size = 0

        # Perform efficient scan
        for progress in manager.scan_storage_efficient(path):
            if progress["status"] == "completed":
                total_files = progress["total_files"]
                total_size = progress["total_size_gb"] * (1024**3)
                hydrated_files = progress["hydrated_files"]
                hydrated_size = progress["hydrated_size_gb"] * (1024**3)
                scan_duration = progress["scan_duration"]
                break

        # Generate report
        if total_files > 0:
            hydration_percentage = (hydrated_files / total_files) * 100
            size_percentage = (
                (hydrated_size / total_size * 100) if total_size > 0 else 0
            )

            status = (
                "✅" if hydration_percentage > 80 else
                "⚠️" if hydration_percentage > 50 else "❌"
            )

            result.append(f"{status} Hydration Summary:")
            result.append(f"  📁 Total files: {total_files:,}")
            result.append(
                f"  💧 Hydrated files: {hydrated_files:,} "
                f"({hydration_percentage:.1f}%)"
            )
            result.append(
                f"  📊 Total size: {self._format_size(int(total_size))}"
            )
            result.append(
                f"  💧 Hydrated size: {self._format_size(int(hydrated_size))} "
                f"({size_percentage:.1f}%)"
            )
            result.append(f"  ⏱️ Scan time: {scan_duration:.1f} seconds")
            result.append(
                f"  🚀 Speed: {total_files/scan_duration:.0f} files/second"
            )

            # Get additional statistics
            stats = manager.get_storage_statistics()
            if stats["file_types"]:
                result.append("\n📋 Top file types by size:")
                for ft in stats["file_types"][:5]:
                    size_str = self._format_size(ft["total_size"])
                    result.append(
                        f"  {ft['file_type'] or 'No extension'}: "
                        f"{ft['count']} files ({size_str})"
                    )

            # Large files report
            large_files = manager.find_large_files(
                min_size_gb=0.1, limit=5)
            if large_files:
                result.append("\n🐘 Largest files:")
                for lf in large_files:
                    hydration_status = "💧" if lf["is_hydrated"] else "❄️"
                    result.append(
                        f"  {hydration_status} {lf['size_gb']:.1f} GB - "
                        f"{os.path.basename(lf['path'])}"
                    )
        else:
            result.append("📭 No files found in the specified path")

        return "\n".join(result)

     def _run_large_scale_scan(self, path: str, max_files: int = None, deep_scan: bool = False) -> str:
        """Run a large-scale hydration scan optimized for big directories.

        Args:
            path: Directory path to scan
            max_files: Maximum number of files to process (optional)
            deep_scan: Whether to perform deep analysis (optional)

        Returns:
            Formatted scan results as string
        """
        try:
            if not os.path.exists(path):
                return f"❌ Path not found: {path}"

            if not os.path.isdir(path):
                return self._check_file_hydration(path)

            # Import large storage manager for advanced scanning
            manager = LargeStorageManager()

            # Quick scan for immediate results
            result = [f"� Large-scale hydration scan for: {path}"]
            result.append("=" * 50)

            total_files = 0
            total_size = 0
            hydrated_files = 0
            hydrated_size = 0

            # Perform efficient scan
            for progress in manager.scan_storage_efficient(path):
                if progress["status"] == "completed":
                    total_files = progress["total_files"]
                    total_size = progress["total_size_gb"] * (1024**3)
                    hydrated_files = progress["hydrated_files"]
                    hydrated_size = progress["hydrated_size_gb"] * (1024**3)
                    scan_duration = progress["scan_duration"]
                    break

            # Generate report
            if total_files > 0:
                hydration_percentage = (hydrated_files / total_files) * 100
                size_percentage = (
                    (hydrated_size / total_size * 100) if total_size > 0 else 0
                )

                status = (
                    "✅" if hydration_percentage > 80 else
                    "⚠️" if hydration_percentage > 50 else "❌"
                )

                result.append(f"{status} Hydration Summary:")
                result.append(f"  📁 Total files: {total_files:,}")
                result.append(
                    f"  💧 Hydrated files: {hydrated_files:,} "
                    f"({hydration_percentage:.1f}%)"
                )
                result.append(
                    f"  📊 Total size: {self._format_size(int(total_size))}"
                )
                result.append(
                    f"  💧 Hydrated size: {self._format_size(int(hydrated_size))} "
                    f"({size_percentage:.1f}%)"
                )
                result.append(f"  ⏱️ Scan time: {scan_duration:.1f} seconds")
                result.append(
                    f"  🚀 Speed: {total_files/scan_duration:.0f} files/second"
                )

                # Get additional statistics
                stats = manager.get_storage_statistics()
                if stats["file_types"]:
                    result.append("\n📋 Top file types by size:")
                    for ft in stats["file_types"][:5]:
                        size_str = self._format_size(ft["total_size"])
                        result.append(
                            f"  {ft['file_type'] or 'No extension'}: "
                            f"{ft['count']} files ({size_str})"
                        )

                # Large files report
                large_files = manager.find_large_files(
                    min_size_gb=0.1, limit=5)
                if large_files:
                    result.append("\n🐘 Largest files:")
                    for lf in large_files:
                        hydration_status = "💧" if lf["is_hydrated"] else "❄️"
                        result.append(
                            f"  {hydration_status} {lf['size_gb']:.1f} GB - "
                            f"{os.path.basename(lf['path'])}"
                        )
            else:
                result.append("📭 No files found in the specified path")

            return "\n".join(result)

        except ImportError:
            # Fallback to basic scan if large storage manager is not available
            return self._check_directory_hydration(path, max_files, deep_scan)
        except (OSError, PermissionError, IOError) as e:
            return f"❌ Error during large-scale scan: {str(e)}"
