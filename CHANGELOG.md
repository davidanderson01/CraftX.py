# Changelog

All notable changes to CraftX.py will be documented in this file.

## [Latest] - 2025-08-15

### 🛡️ Security Enhancements

- **Environment-based Credentials**: Replaced all hardcoded tokens with environment variables
- **GitGuardian Compliance**: Eliminated secret detection warnings
- **Docker Security Hardening**:
  - Non-root users in all containers
  - Latest Python 3.13 with security patches
  - Capability restrictions and read-only filesystems
  - Security-optimized base images

### 🔧 Infrastructure Fixes

- **Docker Compose**: Removed obsolete `version: "3.9"` attribute to eliminate warnings
- **Package Dependencies**: Fixed incorrect package names in requirements.txt
  - `oauth2lib` → `oauthlib` (correct package name)
  - `microsoft-authentication` → `msal` (Microsoft Authentication Library)
- **Virtual Environment**: Confirmed Python 3.13.5 environment with all dependencies
- **Package Installation**: All requirements now install successfully

### 🐳 Docker Infrastructure

- **Production-Ready Containers**: Multi-stage builds with security focus
- **Security-Hardened Compose**: `docker-compose.secure.yml` with enhanced restrictions
- **Ollama Integration**: AI model serving with containerized deployment
- **Health Checks**: Comprehensive monitoring and validation
- **Alternative Dockerfiles**: Distroless, minimal, and Ubuntu variants

### ⛓️ Blockchain Integration

- **Smart Contract Deployment**: Ethereum-based attestation system
- **Contract Verification**: Deployed at `0x06a682b3F91771a251CE6cf801187160abC7b7eF`
- **Decentralized Proof**: Blockchain-based authenticity verification
- **Secure Key Management**: Environment-based private key storage

### 🔧 Infrastructure Improvements  

- **Environment Templates**: `.env.example` and `.env.template` files
- **Enhanced .gitignore**: Comprehensive exclusion patterns
- **Backup Directory Management**: Automated cleanup and organization
- **Git Workflow Optimization**: Resolved merge conflicts and cleaned repository

### 📚 Documentation Updates

- **README.md**: Added Docker installation, security features, environment configuration
- **Website Updates**: Enhanced feature descriptions with latest capabilities
- **Security Documentation**: Comprehensive security best practices guide
- **Testing Guides**: Docker security testing and verification procedures

### 🐛 Bug Fixes

- **Requirements.txt**: Fixed package version compatibility issues
- **Docker Build**: Resolved Ollama version conflicts and hash mismatches
- **Git Conflicts**: Cleaned up merge issues and repository state
- **Case Sensitivity**: Fixed Dockerfile syntax for proper signal handling

### 🚀 Performance & Reliability

- **Latest Python 3.13**: Improved performance and security
- **Optimized Base Images**: Reduced attack surface with minimal containers
- **Health Monitoring**: Container status verification and restart policies
- **Resource Management**: Efficient memory and CPU utilization

## Previous Versions

### [v1.0.0] - Initial Release

- Core AI framework functionality
- Plugin architecture
- Streamlit UI
- Basic storage backends
