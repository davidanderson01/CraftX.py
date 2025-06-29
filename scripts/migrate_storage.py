"""
Migration tool for CraftX.py storage systems.

This tool helps migrate data between different storage backends.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import shutil

# Debug information
print(f"Current file: {__file__}")
print(f"Current directory: {os.getcwd()}")

# Fix: Calculate project root properly - go up one level from scripts directory
script_dir = Path(__file__).parent
project_root = script_dir.parent
print(f"Script directory: {script_dir}")
print(f"Calculated project root: {project_root}")
print(f"Project root exists: {project_root.exists()}")

craftxpy_path = project_root / "craftxpy"
print(f"CraftXPy path: {craftxpy_path}")
print(f"CraftXPy exists: {craftxpy_path.exists()}")

memory_path = craftxpy_path / "memory"
print(f"Memory module path: {memory_path}")
print(f"Memory module exists: {memory_path.exists()}")

# Add to path
sys.path.insert(0, str(project_root))
print(f"Python path: {sys.path[:3]}")  # Show first 3 entries

# Now try the import
try:
    from craftxpy.memory import JSONStorage, SQLiteStorage
    print("Import successful!")
except ImportError as e:
    print(f"Import failed: {e}")
    # Try alternative import method
    try:
        sys.path.insert(0, str(craftxpy_path.parent))
        from craftxpy.memory import JSONStorage, SQLiteStorage
        print("Import successful with alternative method!")
    except ImportError as e2:
        print(f"Alternative import also failed: {e2}")
        sys.exit(1)


class StorageMigrator:
    """Tool for migrating data between storage systems."""

    def __init__(self):
        self.supported_migrations = {
            "json_to_sqlite": self.migrate_json_to_sqlite,
            "sqlite_to_json": self.migrate_sqlite_to_json,
            "backup_current": self.backup_current_storage,
            "restore_backup": self.restore_from_backup
        }

    def list_available_migrations(self) -> List[str]:
        """List all available migration operations."""
        return list(self.supported_migrations.keys())

    def migrate_json_to_sqlite(self, json_path: str = "chat_logs",
                               sqlite_path: str = "craftx.db") -> Dict[str, Any]:
        """Migrate from JSON storage to SQLite.

        Args:
            json_path: Path to JSON storage directory
            sqlite_path: Path to SQLite database file

        Returns:
            Migration result summary
        """
        print(f"🔄 Migrating from JSON ({json_path}) to SQLite ({sqlite_path})")

        # Initialize storage backends
        json_storage = JSONStorage(json_path)
        sqlite_storage = SQLiteStorage(sqlite_path)

        # Get all sessions from JSON storage
        sessions = json_storage.list_sessions()

        if not sessions:
            return {
                "status": "success",
                "message": "No sessions found to migrate",
                "sessions_migrated": 0,
                "messages_migrated": 0
            }

        total_messages = 0
        migrated_sessions = 0

        for session_id in sessions:
            print(f"  Migrating session: {session_id}")

            # Load conversation from JSON
            conversation = json_storage.load_conversation(session_id)

            if not conversation:
                print(f"    ⚠️ No messages found in session {session_id}")
                continue

            # Migrate each message to SQLite
            for message_data in conversation:
                success = sqlite_storage.save_conversation(
                    session_id=session_id,
                    message=message_data.get("message", ""),
                    role=message_data.get("role", "user"),
                    metadata=message_data.get("metadata", {})
                )

                if success:
                    total_messages += 1
                else:
                    print(
                        f"    ❌ Failed to migrate message in session {session_id}")

            migrated_sessions += 1
            print(f"    ✅ Migrated {len(conversation)} messages")

        return {
            "status": "success",
            "message": (
                f"Successfully migrated {migrated_sessions} sessions "
                f"with {total_messages} messages"
            ),
            "sessions_migrated": migrated_sessions,
            "messages_migrated": total_messages
        }

    def migrate_sqlite_to_json(self, sqlite_path: str = "craftx.db",
                               json_path: str = "chat_logs_export") -> Dict[str, Any]:
        """Migrate from SQLite storage to JSON.

        Args:
            sqlite_path: Path to SQLite database file
            json_path: Path to JSON storage directory

        Returns:
            Migration result summary
        """
        print(f"🔄 Migrating from SQLite ({sqlite_path}) to JSON ({json_path})")

        if not os.path.exists(sqlite_path):
            return {
                "status": "error",
                "message": f"SQLite database not found: {sqlite_path}"
            }

        # Initialize storage backends
        sqlite_storage = SQLiteStorage(sqlite_path)
        json_storage = JSONStorage(json_path)

        # Get all sessions from SQLite
        sessions = sqlite_storage.list_sessions()

        if not sessions:
            return {
                "status": "success",
                "message": "No sessions found to migrate",
                "sessions_migrated": 0,
                "messages_migrated": 0
            }

        total_messages = 0
        migrated_sessions = 0

        for session_id in sessions:
            print(f"  Migrating session: {session_id}")

            # Load conversation from SQLite
            conversation = sqlite_storage.load_conversation(session_id)

            if not conversation:
                print(f"    ⚠️ No messages found in session {session_id}")
                continue

            # Migrate each message to JSON
            for message_data in conversation:
                success = json_storage.save_conversation(
                    session_id=session_id,
                    message=message_data.get("message", ""),
                    role=message_data.get("role", "user"),
                    metadata=message_data.get("metadata", {})
                )

                if success:
                    total_messages += 1
                else:
                    print(
                        f"    ❌ Failed to migrate message in session {session_id}")

            migrated_sessions += 1
            print(f"    ✅ Migrated {len(conversation)} messages")

        return {
            "status": "success",
            "message": (
                f"Successfully migrated {migrated_sessions} sessions "
                f"with {total_messages} messages"
            ),
            "sessions_migrated": migrated_sessions,
            "messages_migrated": total_messages
        }

    def backup_current_storage(self, source_path: str = "chat_logs") -> Dict[str, Any]:
        """Create a backup of current storage.

        Args:
            source_path: Path to source storage

        Returns:
            Backup result summary
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{source_path}_backup_{timestamp}"

        print(f"📦 Creating backup: {source_path} -> {backup_path}")
        try:
            if os.path.exists(source_path):
                shutil.copytree(source_path, backup_path)

                # Count backed up files
                backup_files = list(Path(backup_path).glob("*.json"))

                return {
                    "status": "success",
                    "message": f"Backup created successfully at {backup_path}",
                    "backup_path": backup_path,
                    "files_backed_up": len(backup_files)
                }
            else:
                return {
                    "status": "error",
                    "message": f"Source path not found: {source_path}"
                }
        except (OSError, shutil.Error) as e:
            return {
                "status": "error",
                "message": f"Backup failed: {str(e)}"
            }

    def restore_from_backup(
        self, backup_path: str, restore_path: str = "chat_logs"
    ) -> Dict[str, Any]:
        """Restore storage from backup.

        Args:
            backup_path: Path to backup directory
            restore_path: Path to restore to

        Returns:
            Restore result summary
        """
        print(f"📂 Restoring from backup: {backup_path} -> {restore_path}")

        try:
            if not os.path.exists(backup_path):
                return {
                    "status": "error",
                    "message": f"Backup path not found: {backup_path}"
                }

            # Remove existing restore path if it exists
            if os.path.exists(restore_path):
                shutil.rmtree(restore_path)

            # Copy backup to restore path
            shutil.copytree(backup_path, restore_path)

            # Count restored files
            restored_files = list(Path(restore_path).glob("*.json"))

            return {
                "status": "success",
                "message": f"Successfully restored {len(restored_files)} files",
                "files_restored": len(restored_files)
            }

        except (OSError, shutil.Error) as e:
            return {
                "status": "error",
                "message": f"Restore failed: {str(e)}"
            }

    def run_migration(self, migration_type: str, **kwargs) -> Dict[str, Any]:
        """Run a specific migration operation.

        Args:
            migration_type: Type of migration to run
            **kwargs: Migration-specific parameters

        Returns:
            Migration result
        """
        if migration_type not in self.supported_migrations:
            return {
                "status": "error",
                "message": f"Unsupported migration type: {migration_type}",
                "available_types": self.list_available_migrations()
            }

        try:
            migration_func = self.supported_migrations[migration_type]
            return migration_func(**kwargs)
        except (KeyError, TypeError, ValueError) as e:
            return {
                "status": "error",
                "message": f"Migration failed: {str(e)}"
            }


def interactive_migration():
    """Interactive migration tool."""
    print("🔧 CraftX.py Storage Migration Tool")
    print("=" * 40)

    migrator = StorageMigrator()
    available_migrations = migrator.list_available_migrations()

    print("Available migration operations:")
    for i, migration in enumerate(available_migrations, 1):
        print(f"  {i}. {migration.replace('_', ' ').title()}")

    print("  0. Exit")

    while True:
        try:
            choice = input(
                f"\nSelect migration operation (0-{len(available_migrations)}): ")

            if choice == "0":
                print("👋 Goodbye!")
                break

            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(available_migrations):
                migration_type = available_migrations[choice_idx]

                print(
                    f"\n🚀 Running: {migration_type.replace('_', ' ').title()}")

                # Get parameters based on migration type
                kwargs = {}
                if migration_type == "json_to_sqlite":
                    json_path = input(
                        "JSON storage path [chat_logs]: ").strip() or "chat_logs"
                    sqlite_path = input(
                        "SQLite database path [craftx.db]: ").strip() or "craftx.db"
                    kwargs = {"json_path": json_path,
                              "sqlite_path": sqlite_path}

                elif migration_type == "sqlite_to_json":
                    sqlite_path = input(
                        "SQLite database path [craftx.db]: ").strip() or "craftx.db"
                    json_path = input(
                        "JSON export path [chat_logs_export]: ").strip() or "chat_logs_export"
                    kwargs = {"sqlite_path": sqlite_path,
                              "json_path": json_path}

                elif migration_type == "backup_current":
                    source_path = input(
                        "Source path to backup [chat_logs]: ").strip() or "chat_logs"
                    kwargs = {"source_path": source_path}

                elif migration_type == "restore_backup":
                    backup_path = input("Backup path: ").strip()
                    restore_path = input(
                        "Restore to path [chat_logs]: ").strip() or "chat_logs"
                    kwargs = {"backup_path": backup_path,
                              "restore_path": restore_path}

                # Run migration
                result = migrator.run_migration(migration_type, **kwargs)

                # Display result
                if result["status"] == "success":
                    print(f"✅ {result['message']}")
                else:
                    print(f"❌ {result['message']}")

                input("\nPress Enter to continue...")
            else:
                print("❌ Invalid choice")

        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break


if __name__ == "__main__":
    interactive_migration()
