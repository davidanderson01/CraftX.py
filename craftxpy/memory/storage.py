"""Enhanced storage system for CraftX.py with multiple storage backends."""

import json
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path


class StorageBackend(ABC):
    """Abstract base class for storage backends."""

    @abstractmethod  
     def save_conversation(self, session_id: str, message: str, role: str, metadata: Dict = None) -> bool:
        """Save a conversation message."""
        raise NotImplementedError

    @abstractmethod
    def load_conversation(self, session_id: str) -> List[Dict[str, Any]]:
        """Load conversation history."""
        raise NotImplementedError

    @abstractmethod
    def list_sessions(self) -> List[str]:
        """List all sessions."""
        raise NotImplementedError

    @abstractmethod
    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        raise NotImplementedError


class JSONStorage(StorageBackend):
    """File-based JSON storage backend (current implementation)."""

    def __init__(self, path: str = "chat_logs"):
        self.path = Path(path)
        self.path.mkdir(exist_ok=True)

    def save_conversation(self, session_id: str, message: str, role: str,
                          metadata: Dict = None) -> bool:
        """Save conversation to JSON file."""
        filename = self.path / f"{session_id}.json"
        entry = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "message": message,
            "metadata": metadata or {}
        }

        data = []
        if filename.exists():
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError):
                data = []

        data.append(entry)
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False

    def load_conversation(self, session_id: str) -> List[Dict[str, Any]]:
        """Load conversation from JSON file."""
        filename = self.path / f"{session_id}.json"
        if filename.exists():
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def list_sessions(self) -> List[str]:
        """List all JSON session files."""
        return [f.stem for f in self.path.glob("*.json")]

    def delete_session(self, session_id: str) -> bool:
        """Delete JSON session file."""
        filename = self.path / f"{session_id}.json"
        try:
            if filename.exists():
                filename.unlink()
                return True
        except OSError:
            pass
        return False


class SQLiteStorage(StorageBackend):
    """SQLite database storage backend."""

    def __init__(self, db_path: str = "craftx.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize SQLite database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata JSON
                )
            """)

            # Create indexes separately
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_conversations_session_id "
                "ON conversations(session_id)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_conversations_timestamp "
                "ON conversations(timestamp)"
            )

            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata JSON
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS model_configs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_name TEXT UNIQUE NOT NULL,
                    config JSON,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def save_conversation(self, session_id: str, message: str, role: str,
                          metadata: Dict = None) -> bool:
        """Save conversation to SQLite database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Insert conversation
                conn.execute("""
                    INSERT INTO conversations (session_id, role, message, metadata)
                    VALUES (?, ?, ?, ?)
                """, (session_id, role, message, json.dumps(metadata or {})))

                # Update or insert session
                conn.execute("""
                    INSERT OR REPLACE INTO sessions (session_id, created_at, updated_at)
                    VALUES (?, COALESCE(
                        (SELECT created_at FROM sessions WHERE session_id = ?), 
                        CURRENT_TIMESTAMP
                    ), CURRENT_TIMESTAMP)
                """, (session_id, session_id))

                conn.commit()
                return True
        except sqlite3.Error:
            return False

    def load_conversation(self, session_id: str) -> List[Dict[str, Any]]:
        """Load conversation from SQLite database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT role, message, timestamp, metadata
                    FROM conversations
                    WHERE session_id = ?
                    ORDER BY timestamp ASC
                """, (session_id,))

                return [
                    {
                        "role": row["role"],
                        "message": row["message"],
                        "timestamp": row["timestamp"],
                        "metadata": json.loads(row["metadata"] or "{}")
                    }
                    for row in cursor.fetchall()
                ]
        except sqlite3.Error:
            return []

    def list_sessions(self) -> List[str]:
        """List all sessions from SQLite database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT session_id FROM sessions ORDER BY updated_at DESC")
                return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error:
            return []

    def delete_session(self, session_id: str) -> bool:
        """Delete session from SQLite database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "DELETE FROM conversations WHERE session_id = ?", (session_id,))
                conn.execute(
                    "DELETE FROM sessions WHERE session_id = ?", (session_id,))
                conn.commit()
                return True
        except sqlite3.Error:
            return False


class HybridStorage:
    """Hybrid storage system supporting multiple backends."""

    def __init__(self, primary_backend: StorageBackend, secondary_backends: List[StorageBackend] = None):
        self.primary_backend = primary_backend
        self.secondary_backends = secondary_backends or []

    def save_conversation(self, session_id: str, message: str, role: str,
                          metadata: Dict = None) -> bool:
        """Save to primary backend, optionally replicate to secondary backends."""
        success = self.primary_backend.save_conversation(
            session_id, message, role, metadata)

        # Replicate to secondary backends (best effort)
        for backend in self.secondary_backends:
            try:
                backend.save_conversation(session_id, message, role, metadata)
            except (IOError, sqlite3.Error, json.JSONDecodeError):
                pass  # Continue even if secondary storage fails

        return success

    def load_conversation(self, session_id: str) -> List[Dict[str, Any]]:
        """Load from primary backend, fallback to secondary if needed."""
        try:
            data = self.primary_backend.load_conversation(session_id)
            if data:
                return data
        except (IOError, sqlite3.Error, json.JSONDecodeError):
            pass

        # Try secondary backends
        for backend in self.secondary_backends:
            try:
                data = backend.load_conversation(session_id)
                if data:
                    return data
            except (IOError, sqlite3.Error, json.JSONDecodeError):
                continue

        return []

    def list_sessions(self) -> List[str]:
        """List sessions from primary backend."""
        return self.primary_backend.list_sessions()

    def delete_session(self, session_id: str) -> bool:
        """Delete from all backends."""
        success = self.primary_backend.delete_session(session_id)

        for backend in self.secondary_backends:
            try:
                backend.delete_session(session_id)
            except (IOError, sqlite3.Error, json.JSONDecodeError):
                pass

        return success


class StorageManager:
    """Centralized storage manager for CraftX.py."""

    def __init__(self, storage_config: Dict[str, Any] = None):
        self.config = storage_config or {"type": "json", "path": "chat_logs"}
        self.storage = self._create_storage()

    def _create_storage(self) -> StorageBackend:
        """Create storage backend based on configuration."""
        storage_type = self.config.get("type", "json").lower()

        if storage_type == "json":
            return JSONStorage(self.config.get("path", "chat_logs"))
        if storage_type == "sqlite":
            return SQLiteStorage(self.config.get("db_path", "craftx.db"))
        if storage_type == "hybrid":
            # Create hybrid storage with multiple backends
            primary = self._create_backend(
                self.config.get("primary", {"type": "sqlite"}))
            secondary = [
                self._create_backend(backend_config)
                for backend_config in self.config.get("secondary", [])
            ]
            return HybridStorage(primary, secondary)

        # Default fallback
        return JSONStorage("chat_logs")

    def _create_backend(self, config: Dict[str, Any]) -> StorageBackend:
        """Create individual storage backend."""
        backend_type = config.get("type", "json").lower()

        if backend_type == "json":
            return JSONStorage(config.get("path", "chat_logs"))
        if backend_type == "sqlite":
            return SQLiteStorage(config.get("db_path", "craftx.db"))

        raise ValueError(f"Unsupported backend type: {backend_type}")

    def save_conversation(self, session_id: str, message: str, role: str, metadata: Dict = None) -> bool:
        """Save conversation message."""
        return self.storage.save_conversation(session_id, message, role, metadata)

    def load_conversation(self, session_id: str) -> List[Dict[str, Any]]:
        """Load conversation history."""
        return self.storage.load_conversation(session_id)

    def list_sessions(self) -> List[str]:
        """List all sessions."""
        return self.storage.list_sessions()

    def delete_session(self, session_id: str) -> bool:
        """Delete session."""
        return self.storage.delete_session(session_id)


# Example usage configurations
STORAGE_CONFIGS = {
    "json_only": {
        "type": "json",
        "path": "chat_logs"
    },

    "sqlite_only": {
        "type": "sqlite",
        "db_path": "craftx.db"
    },

    "hybrid_json_sqlite": {
        "type": "hybrid",
        "primary": {"type": "sqlite", "db_path": "craftx.db"},
        "secondary": [{"type": "json", "path": "chat_logs_backup"}]
    }
}


if __name__ == "__main__":
    # Example usage
    storage_manager = StorageManager(STORAGE_CONFIGS["sqlite_only"])

    # Save a conversation
    storage_manager.save_conversation("test_session", "Hello!", "user")
    storage_manager.save_conversation("test_session", "Hi there!", "assistant")

    # Load conversation
    history = storage_manager.load_conversation("test_session")
    print(f"Loaded {len(history)} messages")

    # List sessions
    sessions = storage_manager.list_sessions()
    print(f"Available sessions: {sessions}")
