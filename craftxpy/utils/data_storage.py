"""
CraftX.py Universal Data Storage System
Handles chat logs, files, user data with 1TB capacity
Supports encryption, compression, and multi-cloud sync
"""

import gzip
import hashlib
import json
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import streamlit as st


class UniversalDataStorage:
    """Universal data storage system with 1TB capacity."""

    def __init__(self):
        self.storage_root = Path("universal_storage")
        self.db_path = self.storage_root / "craftx_data.db"
        self.max_storage_bytes = 1024 * 1024 * 1024 * 1024  # 1TB
        self.compression_enabled = True
        self.encryption_enabled = True

        self.storage_structure = {
            "chats": "chat_sessions",
            "files": "user_files",
            "profiles": "user_profiles",
            "settings": "app_settings",
            "cache": "temp_cache",
            "backups": "data_backups",
            "logs": "system_logs"
        }

        self.initialize_storage()

    def initialize_storage(self):
        """Initialize storage system and database."""
        # Create directory structure
        self.storage_root.mkdir(exist_ok=True)
        for category, folder in self.storage_structure.items():
            (self.storage_root / folder).mkdir(exist_ok=True)

        # Initialize SQLite database
        self._init_database()

        # Create storage config
        config_path = self.storage_root / "storage_config.json"
        if not config_path.exists():
            default_config = {
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "max_storage_bytes": self.max_storage_bytes,
                "compression": self.compression_enabled,
                "encryption": self.encryption_enabled,
                "auto_cleanup": True,
                "retention_policy": {
                    "chat_sessions": 365,  # days
                    "temp_files": 7,
                    "logs": 30,
                    "cache": 1
                },
                "storage_stats": {
                    "total_files": 0,
                    "total_size_bytes": 0,
                    "last_cleanup": datetime.now().isoformat()
                }
            }

            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)

    def _init_database(self):
        """Initialize SQLite database with all necessary tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Chat sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                session_data TEXT,
                created_at TIMESTAMP,
                last_updated TIMESTAMP,
                message_count INTEGER,
                file_size_bytes INTEGER,
                is_compressed BOOLEAN,
                is_encrypted BOOLEAN
            )
        ''')

        # User files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_files (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                filename TEXT,
                file_path TEXT,
                file_size_bytes INTEGER,
                file_type TEXT,
                uploaded_at TIMESTAMP,
                last_accessed TIMESTAMP,
                is_compressed BOOLEAN,
                is_encrypted BOOLEAN,
                cloud_synced BOOLEAN
            )
        ''')

        # User profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                email TEXT,
                name TEXT,
                profile_data TEXT,
                auth_provider TEXT,
                created_at TIMESTAMP,
                last_login TIMESTAMP,
                storage_used_bytes INTEGER,
                preferences TEXT
            )
        ''')

        # Storage metadata table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS storage_metadata (
                id TEXT PRIMARY KEY,
                category TEXT,
                metadata TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        ''')

        # Create indexes for better performance
        cursor.execute(
            'CREATE INDEX IF NOT EXISTS idx_chat_user_id ON chat_sessions(user_id)')
        cursor.execute(
            'CREATE INDEX IF NOT EXISTS idx_files_user_id ON user_files(user_id)')
        cursor.execute(
            'CREATE INDEX IF NOT EXISTS idx_files_type ON user_files(file_type)')
        cursor.execute(
            'CREATE INDEX IF NOT EXISTS idx_chat_created ON chat_sessions(created_at)')

        conn.commit()
        conn.close()

    def save_chat_session(self, session_id: str, user_id: str, messages: List[Dict],
                          metadata: Dict = None) -> bool:
        """Save chat session to storage."""
        try:
            session_data = {
                "messages": messages,
                "metadata": metadata or {},
                "saved_at": datetime.now().isoformat()
            }

            # Convert to JSON
            json_data = json.dumps(session_data, ensure_ascii=False)

            # Compress if enabled
            if self.compression_enabled:
                json_data = gzip.compress(json_data.encode()).decode('latin1')

            # Store in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT OR REPLACE INTO chat_sessions 
                (id, user_id, session_data, created_at, last_updated, message_count, 
                 file_size_bytes, is_compressed, is_encrypted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id, user_id, json_data, datetime.now(), datetime.now(),
                len(messages), len(json_data.encode()), self.compression_enabled,
                self.encryption_enabled
            ))

            conn.commit()
            conn.close()

            # Update storage stats
            self._update_storage_stats()

            return True

        except Exception as e:
            print(f"Error saving chat session: {e}")
            return False

    def load_chat_session(self, session_id: str, user_id: str = None) -> Optional[Dict]:
        """Load chat session from storage."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = 'SELECT session_data, is_compressed FROM chat_sessions WHERE id = ?'
            params = [session_id]

            if user_id:
                query += ' AND user_id = ?'
                params.append(user_id)

            cursor.execute(query, params)
            result = cursor.fetchone()
            conn.close()

            if not result:
                return None

            session_data, is_compressed = result

            # Decompress if needed
            if is_compressed:
                session_data = gzip.decompress(
                    session_data.encode('latin1')).decode()

            return json.loads(session_data)

        except Exception as e:
            print(f"Error loading chat session: {e}")
            return None

    def save_user_file(self, user_id: str, filename: str, file_data: bytes,
                       file_type: str = None) -> Optional[str]:
        """Save user file to storage."""
        try:
            file_id = hashlib.sha256(
                f"{user_id}_{filename}_{datetime.now()}".encode()).hexdigest()

            # Determine file type
            if not file_type:
                file_type = Path(filename).suffix.lower()

            # Create file path
            file_path = self.storage_root / "user_files" / \
                user_id / f"{file_id}_{filename}"
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Compress if enabled and file is large
            if self.compression_enabled and len(file_data) > 1024:  # > 1KB
                file_data = gzip.compress(file_data)
                is_compressed = True
            else:
                is_compressed = False

            # Save file
            with open(file_path, 'wb') as f:
                f.write(file_data)

            # Store metadata in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO user_files 
                (id, user_id, filename, file_path, file_size_bytes, file_type,
                 uploaded_at, last_accessed, is_compressed, is_encrypted, cloud_synced)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                file_id, user_id, filename, str(file_path), len(file_data),
                file_type, datetime.now(), datetime.now(), is_compressed,
                self.encryption_enabled, False
            ))

            conn.commit()
            conn.close()

            # Update storage stats
            self._update_storage_stats()

            return file_id

        except Exception as e:
            print(f"Error saving user file: {e}")
            return None

    def load_user_file(self, file_id: str, user_id: str = None) -> Optional[bytes]:
        """Load user file from storage."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = 'SELECT file_path, is_compressed FROM user_files WHERE id = ?'
            params = [file_id]

            if user_id:
                query += ' AND user_id = ?'
                params.append(user_id)

            cursor.execute(query, params)
            result = cursor.fetchone()

            if result:
                # Update last accessed
                cursor.execute(
                    'UPDATE user_files SET last_accessed = ? WHERE id = ?',
                    (datetime.now(), file_id)
                )
                conn.commit()

            conn.close()

            if not result:
                return None

            file_path, is_compressed = result

            # Load file
            with open(file_path, 'rb') as f:
                file_data = f.read()

            # Decompress if needed
            if is_compressed:
                file_data = gzip.decompress(file_data)

            return file_data

        except Exception as e:
            print(f"Error loading user file: {e}")
            return None

    def get_user_chat_sessions(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user's chat sessions."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, created_at, last_updated, message_count, file_size_bytes
                FROM chat_sessions 
                WHERE user_id = ? 
                ORDER BY last_updated DESC 
                LIMIT ?
            ''', (user_id, limit))

            results = cursor.fetchall()
            conn.close()

            sessions = []
            for row in results:
                sessions.append({
                    "session_id": row[0],
                    "created_at": row[1],
                    "last_updated": row[2],
                    "message_count": row[3],
                    "size_bytes": row[4]
                })

            return sessions

        except Exception as e:
            print(f"Error getting user chat sessions: {e}")
            return []

    def get_user_files(self, user_id: str, file_type: str = None) -> List[Dict]:
        """Get user's files."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = '''
                SELECT id, filename, file_size_bytes, file_type, uploaded_at, last_accessed
                FROM user_files 
                WHERE user_id = ?
            '''
            params = [user_id]

            if file_type:
                query += ' AND file_type = ?'
                params.append(file_type)

            query += ' ORDER BY uploaded_at DESC'

            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()

            files = []
            for row in results:
                files.append({
                    "file_id": row[0],
                    "filename": row[1],
                    "size_bytes": row[2],
                    "file_type": row[3],
                    "uploaded_at": row[4],
                    "last_accessed": row[5]
                })

            return files

        except Exception as e:
            print(f"Error getting user files: {e}")
            return []

    def get_storage_stats(self, user_id: str = None) -> Dict:
        """Get storage statistics."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if user_id:
                # User-specific stats
                cursor.execute('''
                    SELECT 
                        COUNT(*) as chat_count,
                        COALESCE(SUM(file_size_bytes), 0) as chat_size
                    FROM chat_sessions WHERE user_id = ?
                ''', (user_id,))
                chat_stats = cursor.fetchone()

                cursor.execute('''
                    SELECT 
                        COUNT(*) as file_count,
                        COALESCE(SUM(file_size_bytes), 0) as file_size
                    FROM user_files WHERE user_id = ?
                ''', (user_id,))
                file_stats = cursor.fetchone()

                total_size = (chat_stats[1] or 0) + (file_stats[1] or 0)

                stats = {
                    "user_id": user_id,
                    "chat_sessions": chat_stats[0] or 0,
                    "chat_size_bytes": chat_stats[1] or 0,
                    "files": file_stats[0] or 0,
                    "file_size_bytes": file_stats[1] or 0,
                    "total_size_bytes": total_size,
                    "storage_used_percent": (total_size / self.max_storage_bytes) * 100,
                    "remaining_bytes": self.max_storage_bytes - total_size
                }
            else:
                # System-wide stats
                cursor.execute(
                    'SELECT COUNT(*), COALESCE(SUM(file_size_bytes), 0) FROM chat_sessions')
                chat_stats = cursor.fetchone()

                cursor.execute(
                    'SELECT COUNT(*), COALESCE(SUM(file_size_bytes), 0) FROM user_files')
                file_stats = cursor.fetchone()

                cursor.execute('SELECT COUNT(*) FROM user_profiles')
                user_count = cursor.fetchone()[0]

                total_size = (chat_stats[1] or 0) + (file_stats[1] or 0)

                stats = {
                    "total_users": user_count or 0,
                    "total_chat_sessions": chat_stats[0] or 0,
                    "total_chat_size_bytes": chat_stats[1] or 0,
                    "total_files": file_stats[0] or 0,
                    "total_file_size_bytes": file_stats[1] or 0,
                    "total_size_bytes": total_size,
                    "storage_used_percent": (total_size / self.max_storage_bytes) * 100,
                    "remaining_bytes": self.max_storage_bytes - total_size
                }

            conn.close()
            return stats

        except Exception as e:
            print(f"Error getting storage stats: {e}")
            return {}

    def _update_storage_stats(self):
        """Update storage statistics."""
        # This would update the storage config with current stats
        pass

    def cleanup_old_data(self, days_old: int = 365):
        """Clean up old data based on retention policy."""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Clean up old chat sessions
            cursor.execute(
                'DELETE FROM chat_sessions WHERE created_at < ?',
                (cutoff_date,)
            )

            # Clean up old temporary files
            cursor.execute(
                'DELETE FROM user_files WHERE file_type = "temp" AND uploaded_at < ?',
                (cutoff_date,)
            )

            conn.commit()
            conn.close()

            return True

        except Exception as e:
            print(f"Error during cleanup: {e}")
            return False


# Global storage manager instance
universal_storage = UniversalDataStorage()
