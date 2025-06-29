import json
import logging
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


#
# ─── STORAGE BACKENDS ────────────────────────────────────────────────────────────
#
class StorageBackend(ABC):
    """Abstract interface for all storage backends."""

    @abstractmethod
    def save_conversation(
        self,
        session_id: str,
        message: str,
        role: str,
        metadata: Dict[str, Any] = None
    ) -> bool:
        """
        Save a conversation message to the storage backend.

        Args:
            session_id (str): The unique identifier for the conversation session.
            message (str): The message content to save.
            role (str): The role of the message sender (e.g., 'user', 'assistant').
            metadata (Dict[str, Any], optional): Additional metadata for the message.

        Returns:
            bool: True if the message was saved successfully, False otherwise.
        """
        raise NotImplementedError()

    @abstractmethod
    def load_conversation(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Load all messages for a given conversation session.

        Args:
            session_id (str): The unique identifier for the conversation session.

        Returns:
            List[Dict[str, Any]]: A list of message records for the session.
        """
        raise NotImplementedError()

    @abstractmethod
    def list_sessions(self) -> List[str]:
        """
        List all conversation session identifiers.

        Returns:
            List[str]: A list of session IDs.
        """
        ...

    @abstractmethod
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a conversation session from the storage backend.

        Args:
            session_id (str): The unique identifier for the conversation session.

        Returns:
            bool: True if the session was deleted successfully, False otherwise.
        """
        ...


class JSONStorage(StorageBackend):
    """Simple file-based JSON storage."""

    def __init__(self, path: str = "chat_logs"):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)

    def save_conversation(self, session_id, message, role, metadata=None):
        filename = self.path / f"{session_id}.json"
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "role":    role,
            "message": message,
            "metadata": metadata or {}
        }

        records = []
        if filename.exists():
            try:
                records = json.loads(filename.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                logging.warning("Corrupt JSON; overwriting file: %s", filename)

        records.append(entry)
        try:
            filename.write_text(json.dumps(records, indent=2, ensure_ascii=False),
                                encoding="utf-8")
            return True
        except IOError as e:
            logging.error("Failed to write JSON log: %s", e)
            return False

    def load_conversation(self, session_id):
        filename = self.path / f"{session_id}.json"
        if not filename.exists():
            return []
        try:
            return json.loads(filename.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            logging.error("Failed to load JSON log: %s", e)
            return []

    def list_sessions(self):
        return [p.stem for p in self.path.glob("*.json")]

    def delete_session(self, session_id):
        filename = self.path / f"{session_id}.json"
        try:
            if filename.exists():
                filename.unlink()
                return True
        except OSError as e:
            logging.error("Failed to delete JSON log: %s", e)
        return False


class SQLiteStorage(StorageBackend):
    """SQLite‐backed conversation store."""

    def __init__(self, db_path: str = "craftx.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id          INTEGER PRIMARY KEY,
                    session_id  TEXT NOT NULL,
                    role        TEXT NOT NULL,
                    message     TEXT NOT NULL,
                    timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata    JSON
                );
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_conv_sid ON conversations(session_id);")
            conn.execute("CREATE TABLE IF NOT EXISTS sessions ("
                         " session_id TEXT PRIMARY KEY,"
                         " created_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
                         " updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
                         " metadata JSON"
                         ");")

    def save_conversation(self, session_id, message, role, metadata=None):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO conversations (session_id, role, message, metadata)
                    VALUES (?, ?, ?, ?)
                """, (session_id, role, message, json.dumps(metadata or {})))
                conn.execute("""
                    INSERT INTO sessions (session_id, created_at, updated_at, metadata)
                    VALUES (
                        ?,
                        COALESCE((SELECT created_at FROM sessions WHERE session_id=?), CURRENT_TIMESTAMP),
                        CURRENT_TIMESTAMP,
                        COALESCE((SELECT metadata FROM sessions WHERE session_id=?), JSON('{}'))
                    )
                    ON CONFLICT(session_id) DO UPDATE
                      SET updated_at=excluded.updated_at
                """, (session_id, session_id, session_id))
            return True
        except (sqlite3.DatabaseError, sqlite3.OperationalError, OSError) as e:
            logging.error("SQLite save error: %s", e)
            return False

    def load_conversation(self, session_id):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT role, message, timestamp, metadata
                      FROM conversations
                     WHERE session_id=?
                  ORDER BY timestamp ASC
                """, (session_id,))
                results = []
                for row in cursor:
                    meta = row["metadata"]
                    decoded = json.loads(meta) if isinstance(
                        meta, str) else (meta or {})
                    results.append({
                        "role":      row["role"],
                        "message":   row["message"],
                        "timestamp": row["timestamp"],
                        "metadata":  decoded
                    })
                return results
        except (sqlite3.DatabaseError, sqlite3.OperationalError, OSError, json.JSONDecodeError) as e:
            logging.error("SQLite load error: %s", e)
            return []

    def list_sessions(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                return [r[0] for r in conn.execute(
                    "SELECT session_id FROM sessions ORDER BY updated_at DESC"
                )]
        except (sqlite3.DatabaseError, sqlite3.OperationalError, OSError) as e:
            logging.error("SQLite list_sessions error: %s", e)
            return []

    def delete_session(self, session_id):
        deleted = False
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur1 = conn.execute(
                    "DELETE FROM conversations WHERE session_id=?", (session_id,))
                cur2 = conn.execute(
                    "DELETE FROM sessions      WHERE session_id=?", (session_id,))
                deleted = (cur1.rowcount + cur2.rowcount) > 0
        except (sqlite3.DatabaseError, sqlite3.OperationalError, OSError) as e:
            logging.error("SQLite delete error: %s", e)
        return deleted


#
# ─── HYBRID STORAGE ──────────────────────────────────────────────────────────────
#
class HybridStorage(StorageBackend):
    """
    Wraps a primary backend plus zero or more secondaries.
    - sync_enabled: after a successful primary write, sync to all secondaries (fails != fatal)
    - fallback_enabled: if primary fails, try first secondary as a fallback
    """

    def __init__(
        self,
        primary_backend: StorageBackend,
        secondary_backends: List[StorageBackend] = None,
        sync_enabled: bool = True,
        fallback_enabled: bool = True
    ):
        self.primary_backend = primary_backend
        self.secondary_backends = secondary_backends or []
        self._sync_enabled = sync_enabled
        self._fallback_enabled = fallback_enabled

    def save_conversation(self, session_id, message, role, metadata=None):
        """Save a conversation, with fallback and sync to secondaries."""
        try:
            ok = self.primary_backend.save_conversation(
                session_id, message, role, metadata)
        except (IOError, OSError, sqlite3.DatabaseError) as exc:
            logging.warning("Primary save failed: %s", exc)
            if self._fallback_enabled and self.secondary_backends:
                try:
                    return self.secondary_backends[0].save_conversation(
                        session_id, message, role, metadata
                    )
                except (IOError, OSError, sqlite3.DatabaseError) as ex:
                    logging.error("Fallback save failed: %s", ex)
            return False

        if ok and self._sync_enabled:
            for idx, sb in enumerate(self.secondary_backends):
                try:
                    sb.save_conversation(session_id, message, role, metadata)
                except (IOError, OSError, sqlite3.DatabaseError) as exc:
                    logging.warning(
                        "Sync to secondary %d failed: %s", idx, exc)
        return ok

    def load_conversation(self, session_id):
        """Load a conversation, with fallback to secondaries."""
        try:
            return self.primary_backend.load_conversation(session_id)
        except (IOError, OSError, sqlite3.DatabaseError, json.JSONDecodeError) as exc:
            logging.warning("Primary load failed: %s", exc)
            if self._fallback_enabled:
                for idx, sb in enumerate(self.secondary_backends):
                    try:
                        return sb.load_conversation(session_id)
                    except (IOError, OSError, sqlite3.DatabaseError, json.JSONDecodeError) as ex:
                        logging.warning(
                            "Secondary %d load failed: %s", idx, ex)
        return []

    def list_sessions(self):
        """List all sessions, with fallback to secondary."""
        try:
            return self.primary_backend.list_sessions()
        except (IOError, OSError, sqlite3.DatabaseError) as exc:
            logging.warning("Primary list_sessions failed: %s", exc)
            if self._fallback_enabled and self.secondary_backends:
                try:
                    return self.secondary_backends[0].list_sessions()
                except (IOError, OSError, sqlite3.DatabaseError) as ex:
                    logging.error("Secondary list_sessions failed: %s", ex)
        return []

    def delete_session(self, session_id):
        """Delete a session from all backends (best effort for secondaries)."""
        success = False
        try:
            success = self.primary_backend.delete_session(session_id)
        except (IOError, OSError, sqlite3.DatabaseError) as exc:
            logging.warning("Primary delete failed: %s", exc)
        for idx, sb in enumerate(self.secondary_backends):
            try:
                sb.delete_session(session_id)
            except (IOError, OSError, sqlite3.DatabaseError) as exc:
                logging.warning("Secondary %d delete failed: %s", idx, exc)
        return success


#
# ─── STORAGE MANAGER ─────────────────────────────────────────────────────────────
#
class StorageManager:
    """Factory/Facade over JSON, SQLite, or Hybrid configs."""

    def __init__(self, storage_config: Dict[str, Any] = None):
        self.config = storage_config or {"type": "json", "path": "chat_logs"}
        self.storage = self._create_storage(self.config)

    def _create_storage(self, cfg) -> StorageBackend:
        t = cfg.get("type", "json").lower()
        if t == "json":
            return JSONStorage(cfg.get("path", "chat_logs"))
        if t == "sqlite":
            return SQLiteStorage(cfg.get("db_path", "craftx.db"))
        if t == "hybrid":
            primary = self._create_storage(cfg["primary"])
            second = [self._create_storage(s)
                      for s in cfg.get("secondary", [])]
            return HybridStorage(
                primary, second,
                sync_enabled=cfg.get("sync_enabled", True),
                fallback_enabled=cfg.get("fallback_enabled", True)
            )
        raise ValueError(f"Unsupported storage type: {t}")

    def save_conversation(self, *args, **kw):
        """Save a conversation message using the configured storage backend."""
        return self.storage.save_conversation(*args, **kw)

    def load_conversation(self, session_id: str):
        """Load all messages for a given conversation session from the storage backend."""
        return self.storage.load_conversation(session_id)

    def list_sessions(self):
        """List all conversation session identifiers from the storage backend."""
        return self.storage.list_sessions()

    def delete_session(self, session_id: str):
        """Delete a conversation session from the storage backend."""
        return self.storage.delete_session(session_id)


# ─── EXAMPLES ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # JSON only
    mgr1 = StorageManager({"type": "json", "path": "chat_logs"})
    mgr1.save_conversation("sess1", "Hello", "user")
    print(mgr1.list_sessions())

    # SQLite only
    mgr2 = StorageManager({"type": "sqlite", "db_path": "craftx.db"})
    mgr2.save_conversation("sess2", "Hi!", "assistant")
    print(mgr2.load_conversation("sess2"))

    # Hybrid: primary=SQLite, secondary=JSON
    cfg_hybrid = {
        "type": "hybrid",
        "primary":   {"type": "sqlite", "db_path": "craftx.db"},
        "secondary": [{"type": "json",   "path": "chat_logs"}],
        "sync_enabled":     True,
        "fallback_enabled": True,
    }
    mgr3 = StorageManager(cfg_hybrid)
    mgr3.save_conversation("sess3", "Howdy!", "user")
    print("Hybrid sessions:", mgr3.list_sessions())
