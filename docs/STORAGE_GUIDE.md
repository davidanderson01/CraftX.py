# CraftX.py Storage System Guide

CraftX.py offers a comprehensive and flexible storage system that can adapt to projects of any size, from simple development prototypes to enterprise-scale applications.

## 🗂️ Current Storage System

### **What's Currently Available**

The project currently has a **file-based JSON storage system** that:

- ✅ Stores chat conversations in JSON files
- ✅ Manages sessions with timestamps
- ✅ Supports UTF-8 encoding
- ✅ Has basic session management (create, load, delete, list)
- ✅ Is simple and works well for development

**Current Structure:**

```text
chat_logs/
├── default.json
├── demo_session.json
└── [session_id].json
```

```text
chat_logs/
├── default.json
├── demo_session.json
└── [session_id].json
```

## 🚀 Enhanced Storage System Options

### **1. JSON Storage (Current)**

```python
from craftxpy.memory import JSONStorage

storage = JSONStorage("chat_logs")
storage.save_conversation("session_1", "Hello!", "user")
```

**Best for:**

- Development and prototyping
- Small projects (< 100 sessions)
- Simple deployment scenarios
- Quick setup and testing

**Pros:** Simple, no dependencies, human-readable
**Cons:** Slower with large datasets, no advanced querying

### **2. SQLite Storage (Recommended)**

```python
from craftxpy.memory import SQLiteStorage

storage = SQLiteStorage("craftx.db")
storage.save_conversation("session_1", "Hello!", "user", {"priority": "high"})
```

**Best for:**

- Production applications
- Medium to large projects (1,000-100,000 sessions)
- Applications needing fast queries
- Multi-user scenarios

**Pros:** Fast, reliable, supports complex queries, ACID compliance
**Cons:** Binary format, requires SQLite knowledge for direct access

### **3. Hybrid Storage (Enterprise)**

```python
from craftxpy.memory import HybridStorage, SQLiteStorage, JSONStorage

primary = SQLiteStorage("main.db")
backup = JSONStorage("backup_logs")
storage = HybridStorage(primary, [backup])
```

**Best for:**

- High-reliability applications
- Enterprise deployments
- Applications requiring redundancy
- Migration scenarios

**Pros:** Redundancy, failover capability, best of both worlds
**Cons:** More complex, higher storage requirements

### **4. Storage Manager (Recommended)**

```python
from craftxpy.memory import StorageManager, StorageConfig

# Use predefined configurations
config = StorageConfig.get_config("production_sqlite")
storage = StorageManager(config)
```

**Configuration Profiles:**

- `development`: JSON storage for development
- `production_sqlite`: SQLite for production
- `production_hybrid`: Hybrid SQLite + JSON backup
- `cloud_ready`: Cloud-compatible with local fallback

## 📊 Storage Recommendations by Project Size

### **Small Project** (< 100 sessions, < 10 MB)

```python
# Recommended: JSON Storage
from craftxpy.memory import StorageManager, StorageConfig

storage = StorageManager(StorageConfig.get_config("development"))
```

### **Medium Project** (< 10,000 sessions, 100 MB - 1 GB)

```python
# Recommended: SQLite Storage
from craftxpy.memory import StorageManager, StorageConfig

storage = StorageManager(StorageConfig.get_config("production_sqlite"))
```

### **Large Project** (< 100,000 sessions, 1-10 GB)

```python
# Recommended: Hybrid Storage
from craftxpy.memory import StorageManager, StorageConfig

storage = StorageManager(StorageConfig.get_config("production_hybrid"))
```

### **Enterprise** (Unlimited sessions, > 10 GB)

```python
# Recommended: Cloud-ready Hybrid
from craftxpy.memory import StorageManager, StorageConfig

storage = StorageManager(StorageConfig.get_config("cloud_ready"))
```

## 🔄 Migration Between Storage Systems

### **Upgrade from JSON to SQLite**

```bash
# Use the migration tool
python scripts/migrate_storage.py
```

Or programmatically:

```python
from scripts.migrate_storage import StorageMigrator

migrator = StorageMigrator()
result = migrator.migrate_json_to_sqlite("chat_logs", "craftx.db")
print(result["message"])
```

### **Backup Current Storage**

```python
migrator = StorageMigrator()
result = migrator.backup_current_storage("chat_logs")
```

## 🌐 Cloud Storage Extensions

### **Azure Integration** (Recommended for Azure users)

```python
# Example Azure Blob Storage extension
from azure.storage.blob import BlobServiceClient
from craftxpy.memory import StorageBackend

class AzureBlobStorage(StorageBackend):
    def __init__(self, connection_string: str, container_name: str):
        self.blob_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_name = container_name
    
    def save_conversation(self, session_id: str, message: str, role: str, metadata: dict = None):
        # Implementation for Azure Blob storage
        pass
```

### **AWS S3 Integration**

```python
# Example S3 storage extension
import boto3
from craftxpy.memory import StorageBackend

class S3Storage(StorageBackend):
    def __init__(self, bucket_name: str, region: str = "us-east-1"):
        self.s3 = boto3.client('s3', region_name=region)
        self.bucket_name = bucket_name
```

## 🛠️ Advanced Storage Features

### **1. Vector Storage for AI** (Future Enhancement)

For semantic search and AI-powered features:

```python
# ChromaDB integration example
import chromadb
from craftxpy.memory import StorageBackend

class VectorStorage(StorageBackend):
    def __init__(self, persist_directory: str = "./vector_db"):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("conversations")
```

### **2. Redis Caching** (Performance Enhancement)

For fast session caching:

```python
import redis
from craftxpy.memory import StorageBackend

class RedisCache:
    def __init__(self, host: str = "localhost", port: int = 6379):
        self.redis_client = redis.Redis(host=host, port=port)
    
    def cache_session(self, session_id: str, data: dict, ttl: int = 3600):
        self.redis_client.setex(f"session:{session_id}", ttl, json.dumps(data))
```

### **3. Database Clustering** (Enterprise)

For high-availability deployments:

```python
# PostgreSQL cluster example
class PostgreSQLCluster(StorageBackend):
    def __init__(self, primary_conn: str, replica_conns: list):
        self.primary = psycopg2.connect(primary_conn)
        self.replicas = [psycopg2.connect(conn) for conn in replica_conns]
```

## 📈 Performance Characteristics

Based on testing with 100 messages:

| Storage Type | Write Speed | Read Speed | Storage Size | Complexity |
|--------------|-------------|------------|--------------|------------|
| JSON         | ~1.5s       | Fast       | Larger       | Low        |
| SQLite       | ~2.5s       | Very Fast  | Compact      | Medium     |
| Hybrid       | ~3.0s       | Fast       | Larger       | High       |

> **Note:** Performance varies based on hardware and data size

## 🔧 Configuration Examples

### **Environment Variables**

```bash
# Override storage configuration
export CRAFTX_STORAGE_TYPE=sqlite
export CRAFTX_DB_PATH=/app/data/craftx.db
export CRAFTX_STORAGE_PATH=/app/logs
```

### **Custom Configuration**

```python
custom_config = {
    "type": "hybrid",
    "primary": {
        "type": "sqlite",
        "db_path": "/app/data/primary.db"
    },
    "secondary": [
        {"type": "json", "path": "/app/backup/logs"},
        {"type": "json", "path": "/mnt/remote/backup"}
    ]
}

storage = StorageManager(custom_config)
```

## 🛡️ Security Considerations

### **Data Encryption**

```python
# Example encrypted storage wrapper
import cryptography.fernet
from craftxpy.memory import StorageBackend

class EncryptedStorage(StorageBackend):
    def __init__(self, backend: StorageBackend, encryption_key: bytes):
        self.backend = backend
        self.cipher = Fernet(encryption_key)
    
    def save_conversation(self, session_id: str, message: str, role: str, metadata: dict = None):
        encrypted_message = self.cipher.encrypt(message.encode()).decode()
        return self.backend.save_conversation(session_id, encrypted_message, role, metadata)
```

### **Access Control**

```python
# Example with user-based access control
class SecureStorage(StorageBackend):
    def __init__(self, backend: StorageBackend, user_permissions: dict):
        self.backend = backend
        self.permissions = user_permissions
    
    def save_conversation(self, session_id: str, message: str, role: str, metadata: dict = None):
        user_id = metadata.get("user_id") if metadata else None
        if self.has_permission(user_id, "write"):
            return self.backend.save_conversation(session_id, message, role, metadata)
        return False
```

## 🎯 Quick Start Guide

### **1. For New Projects**

```python
# Start with SQLite for production-ready storage
from craftxpy.memory import StorageManager, StorageConfig

storage = StorageManager(StorageConfig.get_config("production_sqlite"))
```

### **2. For Existing Projects**

```python
# Migrate from current JSON storage
from scripts.migrate_storage import StorageMigrator

migrator = StorageMigrator()
result = migrator.migrate_json_to_sqlite()
print(f"Migration result: {result['message']}")
```

### **3. For Enterprise Projects**

```python
# Use hybrid storage with redundancy
from craftxpy.memory import StorageManager, StorageConfig

storage = StorageManager(StorageConfig.get_config("production_hybrid"))
```

## 📚 Next Steps

1. **Try the Examples**: Run `python examples/storage_demo.py` to see all storage options in action
2. **Migrate Existing Data**: Use `python scripts/migrate_storage.py` for safe migration
3. **Choose Your Configuration**: Select the appropriate storage profile for your needs
4. **Scale as Needed**: Start simple and upgrade as your project grows

The CraftX.py storage system is designed to grow with your project, from simple prototypes to enterprise applications!
