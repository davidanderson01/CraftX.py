#!/usr/bin/env python3
"""
Cache cleanup script for CraftX.py project.
This script resolves pytest import conflicts by cleaning up Python cache files.
"""

import os
import shutil
import sys
from pathlib import Path


def cleanup_cache(project_root):
    """Clean up Python cache files that cause import conflicts."""

    # Directories to clean
    cache_patterns = [
        "__pycache__",
        "*.pyc",
        ".pytest_cache"
    ]

    # Directories to exclude from cleanup
    exclude_patterns = [
        ".venv",
        "venv",
        "env"
    ]

    cleaned_dirs = []

    for root, dirs, files in os.walk(project_root):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if not any(
            pattern in d for pattern in exclude_patterns)]

        # Remove __pycache__ directories
        if "__pycache__" in dirs:
            cache_dir = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(cache_dir)
                cleaned_dirs.append(cache_dir)
                dirs.remove("__pycache__")
            except OSError as e:
                print(f"Warning: Could not remove {cache_dir}: {e}")

        # Remove .pyc files
        for file in files:
            if file.endswith(".pyc"):
                pyc_file = os.path.join(root, file)
                try:
                    os.remove(pyc_file)
                    cleaned_dirs.append(pyc_file)
                except OSError as e:
                    print(f"Warning: Could not remove {pyc_file}: {e}")

    # Remove .pytest_cache
    pytest_cache = os.path.join(project_root, ".pytest_cache")
    if os.path.exists(pytest_cache):
        try:
            shutil.rmtree(pytest_cache)
            cleaned_dirs.append(pytest_cache)
        except OSError as e:
            print(f"Warning: Could not remove {pytest_cache}: {e}")

    return cleaned_dirs


def clear_import_cache():
    """Clear Python's import cache."""
    if hasattr(sys, 'path_importer_cache'):
        sys.path_importer_cache.clear()

    import importlib
    importlib.invalidate_caches()


def main():
    """Main function."""
    project_root = Path(__file__).parent

    print("🧹 Cleaning up Python cache files...")
    cleaned = cleanup_cache(project_root)

    if cleaned:
        print(f"✅ Cleaned {len(cleaned)} cache files/directories:")
        for item in cleaned:
            print(f"   - {item}")
    else:
        print("✅ No cache files to clean")

    print("🔄 Clearing Python import cache...")
    clear_import_cache()

    print("✅ Cache cleanup complete!")
    print("💡 You can now run: python -m pytest tests/ craftx-stack/ -v")


if __name__ == "__main__":
    main()
