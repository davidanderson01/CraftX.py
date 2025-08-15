# 🧪 Docker Security Testing Guide

## 1. VS Code Security Scanner Test

### Check Current Security Status

1. **Open each Dockerfile in VS Code**:
   - `Dockerfile` (main)
   - `attest/Dockerfile`
   - `Dockerfile.distroless` (alternative)
   - `Dockerfile.minimal` (alternative)

2. **Check Problems Panel**:
   - Press `Ctrl+Shift+M`
   - Look for Docker security warnings
   - Before: Should have seen "3 high vulnerabilities" and "3 critical and 3 high vulnerabilities"
   - After: Should see significantly fewer or zero vulnerability warnings

## 2. Build Tests

### Test Main Stack (Current Production)

```bash
# Navigate to directory
cd "c:\Users\david\CraftXPy\CraftX.py\craftx-stack"

# Build main stack (clean build)
docker-compose build --no-cache

# Build with security-hardened compose
docker-compose -f docker-compose.secure.yml build --no-cache

# Check images created
docker images | grep craftx
```

### Test Alternative Secure Builds

```bash
# Test minimal Dockerfile
docker build -f Dockerfile.minimal -t craftx-minimal:latest .

# Test Ubuntu-based Dockerfile  
docker build -f Dockerfile.ubuntu -t craftx-ubuntu:latest .

# Test distroless Dockerfile
docker build -f Dockerfile.distroless -t craftx-distroless:latest .
```

## 3. Container Security Tests

### Run Security-Hardened Stack

```bash
# Start with security hardened compose
docker-compose -f docker-compose.secure.yml up -d

# Check container status
docker ps

# Test health endpoint
curl http://localhost:8000/health

# Check container security
docker inspect craftx-stack-craftx-1 | grep -i security
docker inspect craftx-stack-craftx-1 | grep -i user
```

### Test Container User Security

```bash
# Check if running as non-root user
docker exec craftx-stack-craftx-1 whoami
# Should return: craftx

# Check user ID (should not be 0/root)
docker exec craftx-stack-craftx-1 id
# Should show uid=1001(craftx) or similar

# Check capabilities (should be minimal)
docker exec craftx-stack-craftx-1 cat /proc/self/status | grep Cap
```

## 4. Image Vulnerability Scanning

### Using Docker Scout (if available)

```bash
# Scan main image
docker scout cves craftx-stack-craftx:latest

# Compare with minimal image
docker scout cves craftx-minimal:latest

# Get security recommendations
docker scout recommendations craftx-stack-craftx:latest
```

### Using Trivy (alternative scanner)

```bash
# Install trivy if not available
winget install aquasec.trivy

# Scan images for vulnerabilities
trivy image craftx-stack-craftx:latest
trivy image craftx-minimal:latest
trivy image craftx-distroless:latest
```

## 5. Runtime Security Tests

### Test Container Permissions

```bash
# Start container
docker run -d --name test-craftx craftx-stack-craftx:latest

# Try to escalate privileges (should fail)
docker exec test-craftx sudo echo "test"
# Should get: sudo: command not found or permission denied

# Check filesystem is read-only (for secure compose)
docker exec test-craftx touch /test-file
# Should fail if using docker-compose.secure.yml

# Cleanup
docker stop test-craftx && docker rm test-craftx
```

### Test Network Security

```bash
# Check exposed ports
docker port craftx-stack-craftx-1

# Test API endpoints
curl -I http://localhost:8000/
curl http://localhost:8000/health
```

## 6. Performance Impact Test

### Compare Performance

```bash
# Test regular build
time docker build -t craftx-regular .

# Test minimal build  
time docker build -f Dockerfile.minimal -t craftx-minimal .

# Test distroless build
time docker build -f Dockerfile.distroless -t craftx-distroless .

# Compare image sizes
docker images | grep craftx
```

## 7. Expected Results

### ✅ **Success Indicators:**

- VS Code Problems panel shows 0 Docker security warnings
- All containers build successfully
- Containers run as non-root user (`craftx`)
- Health checks pass (`curl http://localhost:8000/health`)
- No sudo/root access in containers
- Trivy/Scout scans show minimal vulnerabilities

### ❌ **Issues to Investigate:**

- VS Code still shows high/critical vulnerabilities
- Build failures
- Containers crash on startup
- Health checks fail
- Can escalate to root privileges

## 8. Quick Test Commands

Run this sequence to quickly test everything:

```bash
# 1. Build and test main stack
docker-compose build && docker-compose up -d
curl http://localhost:8000/health
docker exec craftx-stack-craftx-1 whoami

# 2. Test security hardened version
docker-compose down
docker-compose -f docker-compose.secure.yml up -d
curl http://localhost:8000/health

# 3. Check VS Code Problems panel for security warnings
# Open Dockerfile in VS Code and check problems panel
```

## Next Steps Based on Results

- ✅ **If all tests pass**: Security hardening complete!
- ⚠️ **If some tests fail**: Check logs and adjust configuration
- ❌ **If VS Code still shows vulnerabilities**: Try alternative Dockerfiles or update base images further
