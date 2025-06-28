"""Tests for CraftX.py agent router functionality.
Tests for CraftX.py agent router functionality.

This test suite covers:
- AgentRouter functionality (registration, routing, error handling)
- Model plugin behavior and compatibility
- Exception handling and edge cases
- Model inheritance and interface compliance
- Dynamic plugin discovery and validation

Note: Import warnings may appear due to dynamic path manipulation,
but tests run successfully when executed directly.
"""

# Standard library imports
import inspect
import os
import sys
import unittest
from typing import List, Type

# Path setup before local imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Local imports with pylint suppression
# pylint: disable=wrong-import-position,import-error
from craftxpy.plugins.wizardcoder import WizardCoder
from craftxpy.plugins.commandr7b import CommandR7B
from craftxpy.plugins.base import BaseModelPlugin
from craftxpy.agents.router import AgentRouter


def discover_plugin_classes() -> List[Type[BaseModelPlugin]]:
    """Dynamically discover all plugin classes that inherit from BaseModelPlugin.

    Returns:
        List of plugin classes found in the craftxpy.plugins module
    """
    plugin_classes = []

    # Import the plugins module to get all available plugins
    try:
        import craftxpy.plugins as plugins_module

        # Get all modules in the plugins package
        plugins_path = os.path.dirname(plugins_module.__file__)

        for filename in os.listdir(plugins_path):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]  # Remove .py extension

                try:
                    # Dynamic import
                    module = __import__(
                        f'craftxpy.plugins.{module_name}', fromlist=[module_name])

                    # Find classes that inherit from BaseModelPlugin
                    for _, obj in inspect.getmembers(module, inspect.isclass):
                        if (issubclass(obj, BaseModelPlugin) and
                            obj != BaseModelPlugin and
                                obj.__module__ == module.__name__):
                            plugin_classes.append(obj)

                except ImportError:
                    continue  # Skip modules that can't be imported

    except ImportError:
        # Fallback to known plugins if dynamic discovery fails
        plugin_classes = [WizardCoder, CommandR7B]

    return plugin_classes


class MockModel(BaseModelPlugin):
    """Mock model for testing purposes."""

    def __init__(self, response_prefix="Mock"):
        """Initialize mock model with response prefix."""
        super().__init__()
        self.response_prefix = response_prefix

    def generate(self, prompt: str) -> str:
        """Generate a mock response."""
        return f"[{self.response_prefix}] Response to: {prompt}"

    def get_capabilities(self) -> dict:
        """Return mock capabilities for testing."""
        return {"task_types": ["text"], "max_tokens": 1000}

    def validate_config(self) -> bool:
        """Validate model configuration."""
        return True


class TestPluginDiscovery(unittest.TestCase):
    """Test cases for dynamic plugin discovery."""

    def setUp(self):
        """Set up test fixtures."""
        self.discovered_plugins = discover_plugin_classes()

    def test_plugin_discovery_finds_plugins(self):
        """Test that plugin discovery finds at least some plugins."""
        self.assertGreater(len(self.discovered_plugins), 0,
                           "Should discover at least one plugin class")

    def test_all_discovered_plugins_inherit_base(self):
        """Test that all discovered plugins inherit from BaseModelPlugin."""
        for plugin_class in self.discovered_plugins:
            with self.subTest(plugin=plugin_class.__name__):
                self.assertTrue(issubclass(plugin_class, BaseModelPlugin),
                                f"{plugin_class.__name__} should inherit from BaseModelPlugin")

    def test_all_plugins_implement_required_methods(self):
        """Test that all plugins implement required abstract methods."""
        required_methods = ['generate', 'get_model_info']

        for plugin_class in self.discovered_plugins:
            with self.subTest(plugin=plugin_class.__name__):
                plugin_instance = plugin_class()

                for method_name in required_methods:
                    self.assertTrue(hasattr(plugin_instance, method_name),
                                    f"{plugin_class.__name__} missing method: {method_name}")
                    self.assertTrue(callable(getattr(plugin_instance, method_name)),
                                    f"{plugin_class.__name__}.{method_name} is not callable")

    def test_plugin_instantiation(self):
        """Test that all discovered plugins can be instantiated."""
        for plugin_class in self.discovered_plugins:
            with self.subTest(plugin=plugin_class.__name__):
                try:
                    plugin_instance = plugin_class()
                    self.assertIsInstance(plugin_instance, BaseModelPlugin)
                    self.assertIsInstance(plugin_instance, plugin_class)
                except (ValueError, TypeError, AttributeError) as e:
                    self.fail(
                        f"Failed to instantiate {plugin_class.__name__}: {e}")

    def test_plugin_generate_method(self):
        """Test that all plugins can generate responses."""
        test_prompt = "Hello, world!"

        for plugin_class in self.discovered_plugins:
            with self.subTest(plugin=plugin_class.__name__):
                plugin_instance = plugin_class()
                response = plugin_instance.generate(test_prompt)

                self.assertIsInstance(response, str,
                                      f"{plugin_class.__name__} should return string response")
                self.assertGreater(len(response), 0,
                                   f"{plugin_class.__name__} should return non-empty response")


class TestAgentRouter(unittest.TestCase):
    """Test cases for the AgentRouter class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.router = AgentRouter()
        self.mock_model = MockModel("TestModel")
        self.discovered_plugins = discover_plugin_classes()

    def tearDown(self):
        """Clean up after each test method."""
        if hasattr(self.router, 'models'):
            self.router.models.clear()

    def test_empty_router_initialization(self):
        """Test that router initializes with empty models dict."""
        router = AgentRouter()
        self.assertEqual(len(router.models), 0)

    def test_router_with_initial_models(self):
        """Test router initialization with models."""
        models = {"test": self.mock_model}
        router = AgentRouter(models=models)
        self.assertEqual(len(router.models), 1)
        self.assertIn("test", router.models)

    def test_register_all_discovered_plugins(self):
        """Test registering all discovered plugins with the router."""
        for i, plugin_class in enumerate(self.discovered_plugins):
            with self.subTest(plugin=plugin_class.__name__):
                task_name = f"task_{plugin_class.__name__.lower()}_{i}"
                plugin_instance = plugin_class()

                self.router.register(task_name, plugin_instance)
                self.assertIn(task_name, self.router.models)
                self.assertEqual(
                    self.router.models[task_name], plugin_instance)

    def test_route_to_all_plugins(self):
        """Test routing to all discovered plugins."""
        test_prompt = "Generate a test response"

        # Register all plugins
        for i, plugin_class in enumerate(self.discovered_plugins):
            task_name = f"task_{plugin_class.__name__.lower()}_{i}"
            plugin_instance = plugin_class()
            self.router.register(task_name, plugin_instance)

        # Test routing to each plugin
        for i, plugin_class in enumerate(self.discovered_plugins):
            with self.subTest(plugin=plugin_class.__name__):
                task_name = f"task_{plugin_class.__name__.lower()}_{i}"
                response = self.router.route(task_name, test_prompt)

                self.assertIsInstance(response, str)
                self.assertGreater(len(response), 0)

    def test_register_model(self):
        """Test registering a model with the router."""
        self.router.register("test_task", self.mock_model)
        self.assertIn("test_task", self.router.models)
        self.assertEqual(self.router.models["test_task"], self.mock_model)

    def test_unregister_model(self):
        """Test unregistering a model from the router."""
        self.router.register("test_task", self.mock_model)
        result = self.router.unregister("test_task")
        self.assertTrue(result)
        self.assertNotIn("test_task", self.router.models)

    def test_route_to_existing_model(self):
        """Test routing to an existing model."""
        self.router.register("test_task", self.mock_model)
        response = self.router.route("test_task", "Hello world")
        self.assertIn("TestModel", response)
        self.assertIn("Hello world", response)

    def test_route_to_nonexistent_model(self):
        """Test routing to a non-existent model."""
        response = self.router.route("nonexistent", "Hello world")
        self.assertIn("No model registered", response)
        self.assertIn("nonexistent", response)

    def test_list_models(self):
        """Test listing registered models."""
        self.router.register("test1", self.mock_model)
        self.router.register("test2", MockModel("SecondModel"))

        models_info = self.router.list_models()
        self.assertEqual(len(models_info), 2)
        self.assertIn("test1", models_info)
        self.assertIn("test2", models_info)


class TestModelPlugins(unittest.TestCase):
    """Test cases for individual model plugins."""

    def setUp(self):
        """Set up test fixtures for model plugin tests."""
        self.discovered_plugins = discover_plugin_classes()

        # Try to instantiate known plugins for specific tests
        try:
            self.base_plugin = MockModel("BasePluginMock")
            self.wizard_plugin = WizardCoder()
            self.commandr_plugin = CommandR7B()
        except ImportError as e:
            self.skipTest(f"Required modules not available: {e}")

    def test_plugin_interface_compliance(self):
        """Test that all plugins comply with the base interface."""
        for plugin_class in self.discovered_plugins:
            with self.subTest(plugin=plugin_class.__name__):
                plugin = plugin_class()

                # Test required attributes
                self.assertTrue(hasattr(plugin, 'model_name'))

                # Test required methods
                self.assertTrue(hasattr(plugin, 'generate'))
                self.assertTrue(hasattr(plugin, 'get_model_info'))

                # Test method signatures
                info = plugin.get_model_info()
                self.assertIsInstance(info, dict)
                self.assertIn('name', info)

    def test_plugin_model_info_structure(self):
        """Test that plugin model info has expected structure."""
        expected_keys = ['name', 'version', 'description']

        for plugin_class in self.discovered_plugins:
            with self.subTest(plugin=plugin_class.__name__):
                plugin = plugin_class()
                info = plugin.get_model_info()

                for key in expected_keys:
                    self.assertIn(key, info,
                                  f"{plugin_class.__name__} model info missing key: {key}")

    def test_wizardcoder_plugin(self):
        """Test WizardCoder plugin specifically."""
        model = WizardCoder()
        response = model.generate("Write a function")
        self.assertIn("WizardCoder", response)
        self.assertIn("Write a function", response)

    def test_commandr7b_plugin(self):
        """Test CommandR7B plugin specifically."""
        model = CommandR7B()
        response = model.generate("Explain AI")
        self.assertIn("CommandR7B", response)
        self.assertIn("Explain AI", response)


class TestPluginRegistry(unittest.TestCase):
    """Test cases for plugin registry functionality."""

    def setUp(self):
        """Set up plugin registry tests."""
        self.discovered_plugins = discover_plugin_classes()

    def test_plugin_registry_completeness(self):
        """Test that plugin registry includes all expected plugins."""
        expected_plugins = ['WizardCoder', 'CommandR7B']
        discovered_names = [cls.__name__ for cls in self.discovered_plugins]

        for expected in expected_plugins:
            self.assertIn(expected, discovered_names,
                          f"Expected plugin {expected} not found in discovery")

    def test_no_duplicate_plugins(self):
        """Test that no duplicate plugins are discovered."""
        plugin_names = [cls.__name__ for cls in self.discovered_plugins]
        unique_names = set(plugin_names)

        self.assertEqual(len(plugin_names), len(unique_names),
                         "Duplicate plugins found in discovery")


def run_comprehensive_tests():
    """Run all tests with detailed output and plugin discovery info."""
    print("🧪 Running CraftX.py Comprehensive Test Suite")
    print("=" * 50)

    # Show discovered plugins
    discovered = discover_plugin_classes()
    print(f"🔍 Discovered {len(discovered)} plugin classes:")
    for plugin_class in discovered:
        print(f"  • {plugin_class.__name__} ({plugin_class.__module__})")
    print()

    # Create comprehensive test suite
    test_suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestPluginDiscovery,
        TestAgentRouter,
        TestModelPlugins,
        TestPluginRegistry
    ]

    for test_class in test_classes:
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_class))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print comprehensive summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"  • Tests run: {result.testsRun}")
    print(f"  • Failures: {len(result.failures)}")
    print(f"  • Errors: {len(result.errors)}")
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) -
                        len(result.errors)) / result.testsRun * 100)
        print(f"  • Success rate: {success_rate:.1f}%")

    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed")

        if result.failures:
            print("\n🚨 Failures:")
            for test, traceback in result.failures:
                error_msg = traceback.split(
                    'AssertionError: ')[-1].split('\n')[0]
                print(f"  • {test}: {error_msg}")

        if result.errors:
            print("\n💥 Errors:")
            for test, traceback in result.errors:
                error_msg = traceback.split(
                    '\n')[-2] if traceback.split('\n') else "Unknown error"
                print(f"  • {test}: {error_msg}")

    return result.wasSuccessful()


if __name__ == "__main__":
    sys.exit(0 if run_comprehensive_tests() else 1)
