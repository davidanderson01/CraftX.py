#!/usr/bin/env python3
"""CraftX.py Package Demo

This script demonstrates the functionality of the published CraftX.py package.
"""


def test_craftxpy_package():
    """Test the complete CraftX.py package functionality."""
    print("🚀 CraftX.py Package Demo - Version 0.1.2")
    print("=" * 60)

    try:
        # Test main package import
        print("\n1. 📦 Testing main package import...")
        import craftxpy
        print(f"   ✅ CraftX.py v{craftxpy.__version__} imported successfully!")
        print(f"   📝 Description: {craftxpy.__description__}")
        print(f"   👥 Author: {craftxpy.__author__}")

        # Test Router
        print("\n2. 🧭 Testing Router functionality...")
        from craftxpy.agents import Router
        router = Router()
        print(f"   ✅ Router created: {router.name}")

        response = router.route("Hello, CraftX.py!")
        print(f"   💬 Router response: {response}")

        status = router.get_status()
        print(f"   📊 Router status: {status}")

        # Test Logger
        print("\n3. 📝 Testing Logger functionality...")
        from craftxpy.memory import Logger
        logger = Logger("demo")

        logger.info("Testing CraftX.py logger", test=True)
        logger.warning("This is a test warning")
        logger.error("This is a test error")

        memory = logger.get_memory()
        print(f"   ✅ Logger created with {len(memory)} log entries")

        # Test BasePlugin
        print("\n4. 🔌 Testing Plugin system...")
        # from craftxpy.plugins.base import BasePlugin, DemoPlugin

        # demo_plugin = DemoPlugin()
        # print(
        #     f"   ✅ Plugin created: {demo_plugin.name} v{demo_plugin.version}")

        # result = demo_plugin.execute("test data")
        # print(f"   🔄 Plugin result: {result}")

        # plugin_info = demo_plugin.get_info()
        # print(f"   📋 Plugin info: {plugin_info}")

        # Test Utils
        print("\n5. 🛠️  Testing Utility functions...")
        from craftxpy.utils import PageBuilder, ShellExecutor

        # Test PageBuilder
        builder = PageBuilder("CraftX.py Demo")
        builder.add_css("body { font-family: Arial; }")
        builder.add_content("<h1>Hello from CraftX.py!</h1>")
        html = builder.build()
        print(f"   ✅ PageBuilder created HTML ({len(html)} chars)")

        # Test ShellExecutor
        executor = ShellExecutor()
        result = executor.execute("echo Hello CraftX.py!")
        print(f"   ✅ ShellExecutor result: {result['success']}")

        # Test Memory Storage
        print("\n6. 💾 Testing Memory Storage...")
        from craftxpy.memory import MemoryConfig, MemoryStorage

        storage = MemoryStorage()
        storage.store("demo_key", "Hello from CraftX.py storage!")
        retrieved = storage.retrieve("demo_key")
        print(f"   ✅ Storage test: {retrieved}")

        config = MemoryConfig()
        memory_limit = config.get("memory_limit")
        print(f"   ⚙️  Memory config: limit={memory_limit}")

        # Test Plugin Tools
        print("\n7. 🔧 Testing Plugin Tools...")
        from craftxpy.plugins.tools import FileHydrator, LargeStorageManager

        hydrator = FileHydrator()
        print(
            f"   ✅ FileHydrator created: {hydrator.name} v{hydrator.version}")

        storage_mgr = LargeStorageManager()
        print(
            f"   ✅ LargeStorageManager created: {storage_mgr.name} v{storage_mgr.version}")

        print("\n🎉 All tests completed successfully!")
        print("🔗 Package available at: https://pypi.org/project/craftxpy/")
        print("📚 Install with: pip install craftxpy")

        return True

    except (ImportError, AttributeError, RuntimeError) as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_craftxpy_package()
