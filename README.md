# CraftX.py

**Python-native intelligence, modular by design.**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-blue)](https://github.com/davidanderson01/craftxpy)

CraftX.py is a modular AI scripting framework designed specifically for Python developers. It provides seamless integration with multiple AI models, secure automation tools, and an extensible plugin architecture.

## 🚀 Features

- **🤖 Multi-Model Support**: Integrate WizardCoder, CommandR7B, CodeGeeX4, and Qwen2.5-Coder
- **🔧 Modular Tools**: Extensible plugin system with built-in utilities
- **🛡️ Secure Execution**: Safe shell commands with whitelist protection
- **💾 Memory System**: Persistent conversation history and session management
- **🎨 Beautiful UI**: Modern Streamlit-based interface
- **🐍 Python-Native**: Clean APIs with type hints and pythonic design

## 📦 Installation

### Quick Start

```bash
git clone https://github.com/davidanderson01/craftxpy.git
cd craftxpy
pip install -r requirements.txt
```

### Development Installation

```bash
pip install -e .[dev]
```

## 🎯 Quick Start

### 1. Basic Usage

```python
from craftxpy.agents.router import AgentRouter
from craftxpy.plugins.wizardcoder import WizardCoder

# Initialize AI model router
router = AgentRouter({"codegen": WizardCoder()})

# Generate code
response = router.route("codegen", "Create a FastAPI endpoint for user auth")
print(response)
```

### 2. Web Interface

```bash
streamlit run assistant_ui/app.py
```

### 3. Run Demo

```bash
python examples/demo.py
```

## 🏗️ Architecture

```text
craftxpy/
├── agents/          # AI model routing and management
├── plugins/         # Model integrations and tools
│   ├── wizardcoder.py
│   ├── commandr7b.py
│   ├── codegeex4.py
│   ├── qwen25coder.py
│   └── tools/       # Extensible tool plugins
├── memory/          # Conversation logging and history
├── utils/           # Utilities (shell, page builder)
└── assistant_ui/    # Streamlit web interface
```

## 🔧 Built-in Tools

- **🌐 DNS Validator**: Validate domain resolution
- **🔒 SSL Checker**: Check certificate status and expiration
- **📁 File Monitor**: Monitor OneDrive file hydration (Windows)
- **🛠️ Custom Tools**: Easy plugin creation system

## 💡 Creating Custom Tools

```bash
python scripts/new_tool.py "My Custom Tool"
```

Or programmatically:

```python
from craftxpy.plugins.tools.base_tool import BaseTool

class MyTool(BaseTool):
    def run(self, **kwargs) -> str:
        return "✅ Tool executed successfully!"
```

## 🎨 Web Interface

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

- **Website**: [https://craftx.py](https://craftx.py)
- **Documentation**: [https://docs.craftx.py](https://docs.craftx.py)

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_router.py
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/davidanderson01/craftxpy.git
cd craftxpy
pip install -e .[dev]
pre-commit install
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AI Models**: Thanks to the teams behind WizardCoder, CommandR7B, CodeGeeX4, and Qwen2.5-Coder
- **Framework**: Built with Streamlit, Python, and modern web technologies
- **Community**: Special thanks to all contributors and early adopters

## 🔗 Links

- **GitHub**: [github.com/davidanderson01/craftxpy](https://github.com/davidanderson01/craftxpy)
- **PyPI**: [pypi.org/project/craftxpy](https://pypi.org/project/craftxpy)
- **Docker**: [hub.docker.com/r/craftx/craftxpy](https://hub.docker.com/r/craftx/craftxpy)

---

![CraftX.py Logo](assets/img/craftx-logo.png)

**CraftX.py** - *Python-native intelligence, modular by design.*

[Get Started](https://docs.craftx.py) • [Documentation](https://docs.craftx.py/docs) • [Examples](examples/) • [Community](https://github.com/davidanderson01/craftxpy/discussions)
