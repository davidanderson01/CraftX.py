# Welcome to CraftX.py

**Python-native intelligence, modular by design.**

CraftX.py is a powerful, modular AI scripting framework built specifically for Python developers. It provides seamless integration with multiple AI models, secure automation capabilities, and an extensible plugin architecture.

## 🚀 What makes CraftX.py special?

### Multi-Model Support

Integrate and switch between different AI models:

- **WizardCoder** - Advanced code generation
- **CommandR7B** - Powerful reasoning and instruction following  
- **CodeGeeX4** - Multilingual code generation
- **Qwen2.5-Coder** - State-of-the-art coding assistance

### Modular Architecture

```python
from craftxpy.agents.router import AgentRouter
from craftxpy.plugins.wizardcoder import WizardCoder

# Route tasks to appropriate models
router = AgentRouter({
    "codegen": WizardCoder(),
    "debugging": CommandR7B()
})

response = router.route("codegen", "Create a FastAPI endpoint")
```

### Built-in Tools

- **🌐 DNS Validator** - Check domain resolution
- **🔒 SSL Certificate Checker** - Monitor certificate status
- **📁 File Hydration Monitor** - OneDrive file status (Windows)
- **🛠️ Custom Tool System** - Easy plugin creation

### Security First

- Whitelisted shell commands for safe automation
- Input validation and sanitization
- Session isolation and error handling

## 📦 Quick Installation

```bash
git clone https://github.com/davidanderson01/craftxpy.git
cd craftxpy
pip install -r requirements.txt
```

## 🎯 Quick Start

### 1. Basic Usage

```python
from craftxpy.agents.router import AgentRouter
from craftxpy.plugins.wizardcoder import WizardCoder

router = AgentRouter({"ai": WizardCoder()})
result = router.route("ai", "Write a Python function to validate email")
print(result)
```

### 2. Web Interface

```bash
streamlit run assistant_ui/app.py
```

### 3. Run Examples

```bash
python examples/demo.py
```

## 🔧 Core Components

- **Agents** - Smart routing and model management
- **Plugins** - Extensible AI model integrations
- **Tools** - Utility functions and system integrations
- **Memory** - Conversation history and session persistence
- **Utils** - Helper functions for common tasks

## 🎨 Features

✅ **Multiple AI Models** - Switch between different models based on task  
✅ **Secure Shell** - Whitelisted command execution  
✅ **Plugin System** - Easy tool creation and integration  
✅ **Web Interface** - Beautiful Streamlit-based UI  
✅ **Memory System** - Persistent conversation history  
✅ **Type Safety** - Full type hints throughout  
✅ **Python Native** - Built for Python developers  

## 📚 Next Steps

- [Installation Guide](./installation) - Detailed setup instructions
- [API Reference](./api) - Complete API documentation  
- [Plugin Development](./plugins) - Create custom tools
- [Examples](./examples) - Real-world usage examples
- [Contributing](./contributing) - Join the community

---

Ready to build intelligent Python applications? Let's get started! 🚀
