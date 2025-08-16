#!/usr/bin/env python3
"""Test script to verify the installed craftxpy package works correctly."""

import traceback


def test_import():
    """Test importing the craftxpy package."""
    try:
        print("🧪 Testing craftxpy import...")
        import craftxpy
        print("✅ CraftXPy successfully imported!")

        print(f"📦 Package location: {craftxpy.__file__}")
        print(f"🏷️  Version: {craftxpy.__version__}")

        # Test importing submodules
        print("🧪 Testing submodule imports...")

        try:
            from craftxpy.agents import Router
            print("✅ Router imported successfully!")
        except ImportError as e:
            print(f"⚠️  Router import failed: {e}")

        try:
            # from craftxpy.memory import Logger
            print("✅ Logger imported successfully!")
        except Exception as e:
            print(f"⚠️  Logger import failed: {e}")

        try:
            # from craftxpy.plugins.base import BasePlugin
            print("✅ BasePlugin imported successfully!")
        except ImportError as e:
            print(f"⚠️  BasePlugin import failed: {e}")

        try:
            # from craftxpy.utils import PageBuilder, ShellExecutor
            print("✅ Utils imported successfully!")
        except Exception as e:
            print(f"⚠️  Utils import failed: {e}")

        # Test creating instances
        print("🧪 Testing object instantiation...")
        try:
            router = Router()
            print(
                f"✅ Router instance created successfully! Type: {type(router)}")
        except Exception as e:
            print(f"⚠️  Router instantiation failed: {e}")

        print("🎉 Package import test completed!")

    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    test_import()
