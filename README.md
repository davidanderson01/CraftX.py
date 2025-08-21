# CraftX.py

![CraftX.py Logo](assets/img/craftx-logo.svg)

[![PyPI version](https://badge.fury.io/py/craftxpy.svg)](https://badge.fury.io/py/craftxpy)
[![Python Version](https://img.shields.io/pypi/pyversions/craftxpy.svg)](https://pypi.org/project/craftxpy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/craftxpy)](https://pepy.tech/project/craftxpy)
[![Netlify Status](https://api.netlify.com/api/v1/badges/harmonious-naiad-3cd735/deploy-status)](https://app.netlify.com/sites/harmonious-naiad-3cd735/deploys)

**Python-native intelligence, modular by design.**

🌐 **Live Demo**: [https://harmonious-naiad-3cd735.netlify.app](https://harmonious-naiad-3cd735.netlify.app) | 📚 **Documentation**: [docs.craftx.py](https://docs.craftx.py) | 🔗 **PyPI**: [craftxpy](https://pypi.org/project/craftxpy/)

[Installation](#-installation) • [Quick Start](#-quick-start) • [Authentication](#-authentication--security) • [Documentation](#-documentation) • [Examples](#-examples) • [Support](#-support)

## 💖 Support

If you find CraftX.py helpful, please consider supporting the project:

[![Sponsor on GitHub](https://img.shields.io/badge/Sponsor_on_GitHub-F7514A?style=for-the-badge&logo=github-sponsors&logoColor=white)](https://github.com/sponsors/davidanderson01)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy_Me_a_Coffee-yellow?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://coff.ee/honnalulu0c)

**Your support enables:** 🔧 Maintenance • 🤖 New AI models • 📦 Plugin development • 📚 Documentation • 🐛 Bug fixes • 🔐 Security updates

[Learn more about sponsoring →](SPONSORS.md)

## 🚀 What is CraftX.py?

CraftX.py is a modular, Python-native AI framework designed for building intelligent applications with ease. It provides a clean, extensible architecture for integrating multiple AI models, managing conversations, and extending functionality through plugins.

### ✨ Key Features

- **🔌 Multi-Model Support**: Works with OpenAI, Claude, Ollama, and more
- **🧩 Plugin Architecture**: Extensible system for custom functionality
- **💾 Flexible Storage**: JSON, SQLite, and hybrid storage backends
- **🎨 Modern UI**: Beautiful Streamlit-based interface with OAuth authentication
- **🛡️ Security First**: Command whitelisting, input validation, and environment-based credentials
- **🐳 Docker Ready**: Security-hardened containers with non-root users
- **⛓️ Blockchain Integration**: Ethereum smart contract deployment and attestation
- **📱 Cross-Platform**: Works on Windows, macOS, and Linux
- **🔐 Environment Security**: GitGuardian-compliant credential management
- **🔑 OAuth Authentication**: Multi-provider OAuth (GitHub, Google, Okta, ORCID) + WebAuthn passkeys
- **☁️ Serverless Ready**: Netlify Functions for scalable cloud deployment

## 🔐 Authentication & Security

CraftX.py includes a comprehensive authentication system deployed on Netlify:

### Multi-Provider OAuth Support

- **GitHub OAuth** - Developer-friendly authentication
- **Google OAuth** - Universal access with Google accounts
- **Okta OAuth** - Enterprise SSO integration
- **ORCID OAuth** - Academic and research authentication

### WebAuthn Passkey Authentication

- **FIDO2/WebAuthn** - Modern passwordless authentication
- **Hardware Security Keys** - Support for YubiKey, TouchID, Windows Hello
- **Cross-Platform** - Works on desktop and mobile devices

### Security Features

- **JWT Session Management** - Secure token-based sessions
- **CORS Protection** - Cross-origin request security
- **CSP Headers** - Content Security Policy enforcement
- **Environment Variables** - Secure credential management
- **Serverless Architecture** - No persistent server state

**🌐 Live Demo**: [Try the authentication system](https://harmonious-naiad-3cd735.netlify.app)

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

### 🐳 Docker Installation (Recommended for Production)

CraftX.py includes security-hardened Docker containers:

```bash
# Clone and setup
git clone https://github.com/davidanderson01/CraftX.py.git
cd CraftX.py/craftx-stack

# Create environment file
cp .env.template .env
# Edit .env with your configuration

# Build and run with Docker Compose
docker-compose up -d

# Or use security-hardened version
docker-compose -f docker-compose.secure.yml up -d
```

**Docker Features:**

- 🛡️ Security-hardened containers (non-root users, capability restrictions)
- 🐍 Latest Python 3.13 with security patches
- 🤖 Ollama AI model serving
- 🔐 Environment-based credential management
- 📊 Health checks and monitoring

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

## 🛡️ Security

CraftX.py follows security best practices:

### Credential Management

- ✅ **Environment Variables**: All sensitive data stored in environment variables
- ✅ **GitGuardian Compliant**: No hardcoded secrets in repository
- ✅ **Template Files**: `.env.example` provided for easy setup

### Docker Security

- ✅ **Non-root Users**: All containers run as non-privileged users
- ✅ **Security Patches**: Latest Python and Alpine Linux with security updates
- ✅ **Capability Restrictions**: Minimal container capabilities
- ✅ **Read-only Filesystems**: Immutable container runtime

### Blockchain Security

- ✅ **Smart Contract Attestation**: Ethereum-based proof of authenticity
- ✅ **Secure Key Management**: Private keys via environment variables
- ✅ **Contract Verification**: Deployed contract validation

## 🧪 Testing

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

### Environment Variables

For security, CraftX.py uses environment variables for sensitive data:

```bash
# Copy the example file
cp .env.example .env

# Edit with your credentials
GOOGLE_DRIVE_AUTH_TOKEN=your_google_drive_token
ONEDRIVE_AUTH_TOKEN=your_onedrive_token  
ICLOUD_AUTH_TOKEN=your_icloud_token
RPC_URL=your_ethereum_rpc_url
CONTRACT_ADDRESS=your_deployed_contract_address
PRIVATE_KEY=your_ethereum_private_key
```

### Python Configuration

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
