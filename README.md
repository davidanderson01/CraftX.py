# CraftX.py

![CraftX.py Logo](assets/img/craftx-logo.png)

[![PyPI version](https://badge.fury.io/py/craftxpy.svg)](https://badge.fury.io/py/craftxpy)
[![Python Version](https://img.shields.io/pypi/pyversions/craftxpy.svg)](https://pypi.org/project/craftxpy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/craftxpy)](https://pepy.tech/project/craftxpy)

**Python-native intelligence, modular by design.**

[Installation](#-installation) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Examples](#-examples) • [Support](#-support-craftxpy)

## 💖 Support CraftX.py

If you find CraftX.py helpful, please consider supporting the project:

[![Sponsor on GitHub](https://img.shields.io/badge/Sponsor_on_GitHub-F7514A?style=for-the-badge&logo=github-sponsors&logoColor=white)](https://github.com/sponsors/davidanderson01)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy_Me_a_Coffee-yellow?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://coff.ee/honnalulu0c)

**Your support enables:** 🔧 Maintenance • 🤖 New AI models • 📦 Plugin development • 📚 Documentation • 🐛 Bug fixes

[Learn more about sponsoring →](SPONSORS.md)

## 🚀 What is CraftX.py?

CraftX.py is a modular, Python-native AI framework designed for building intelligent applications with ease. It provides a clean, extensible architecture for integrating multiple AI models, managing conversations, and extending functionality through plugins.

### ✨ Key Features

- **🔌 Multi-Model Support**: Works with OpenAI, Claude, Ollama, and more
- **🧩 Plugin Architecture**: Extensible system for custom functionality
- **💾 Flexible Storage**: JSON, SQLite, and hybrid storage backends
- **🎨 Modern UI**: Beautiful Streamlit-based interface
- **🛡️ Security First**: Command whitelisting and input validation
- **📱 Cross-Platform**: Works on Windows, macOS, and Linux

## 📦 Installation

### Quick Install from PyPI

```bash
pip install craftxpy
```

### Development Installation

```bash
git clone https://github.com/davidanderson01/CraftX.py.git
cd CraftX.py
pip install -e .[dev]
```

## 🚀 Quick Start

```python
import craftxpy

# Initialize the framework
from craftxpy.agents import Router
from craftxpy.memory import Logger

# Create a router for handling messages
router = Router()

# Set up memory logging
logger = Logger()

# Process a message
response = router.route_message("Hello, CraftX.py!")
print(response)
```

## 🎨 Web Interface

Launch the Streamlit interface:

```bash
streamlit run assistant_ui/app.py
```

The Streamlit-based interface provides:

- **Real-time Chat**: Interactive AI conversations
- **Model Switching**: Choose between different AI models
- **Tool Integration**: Access all tools through the UI
- **Session Management**: Persistent conversation history
- **Developer Mode**: Safe shell execution and debugging

## 🛡️ Security Features

- **Command Whitelisting**: Only approved shell commands can execute
- **Input Validation**: All inputs are validated and sanitized
- **Error Handling**: Comprehensive error handling and logging
- **Session Isolation**: Each session is isolated and secure

## 📚 Documentation

- **Website**: [https://craftx.elevatecraft.org](https://craftx.elevatecraft.org)
- **Documentation**: [https://craftx.elevatecraft.org](https://craftx.elevatecraft.org)

## 🧪 Testing

```bash
# Run all tests with beautiful output
python run_tests.py

# Run with pytest
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_ui.py::test_logo_files -v
```

## 🌐 Static Website

The project includes a complete static website:

```bash
# View locally
python -m http.server 8000
# Visit: http://localhost:8000
```

The website is also GitHub Pages ready with automatic deployment.

## 🌟 Examples

Check out our example implementations in the [`examples/`](examples/) directory:

- **Storage Demo** - Showcase different storage backends
- **Large Storage Demo** - Handle big datasets efficiently
- **Plugin Examples** - Custom plugin development

## 🔧 Configuration

CraftX.py supports multiple configuration options:

```python
from craftxpy.memory import Config

config = Config({
    "storage_backend": "sqlite",
    "model_provider": "ollama",
    "debug_mode": True
})
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/davidanderson01/CraftX.py.git
cd CraftX.py
pip install -e .[dev]
pre-commit install
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **GitHub**: [github.com/davidanderson01/CraftX.py](https://github.com/davidanderson01/CraftX.py.git)
- **PyPI**: [pypi.org/project/craftxpy](https://pypi.org/project/craftxpy)
- **Issues**: [GitHub Issues](https://github.com/davidanderson01/CraftX.py/issues)
- **Discussions**: [GitHub Discussions](https://github.com/davidanderson01/CraftX.py/discussions)

---

**Made with ❤️ by [ElevateCraft](https://elevatecraft.org)**

[⭐ Star us on GitHub](https://github.com/davidanderson01/CraftX.py) • [💖 Sponsor this project](https://github.com/sponsors/davidanderson01)
