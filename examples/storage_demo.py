"""
Storage System Examples for CraftX.py

This script demonstrates different storage options available in CraftX.py
and helps you choose the right storage backend for your needs.
"""

import os
import sys
import time
import shutil
import traceback  # Move this to the top with other imports

# Try importing from local path if craftxpy.memory is not installed as a package
try:
    from craftxpy.memory import (
        StorageManager,
        StorageConfig,
        recommend_storage_config,
        JSONStorage,
        SQLiteStorage,
        HybridStorage
    )
except ModuleNotFoundError:
    sys.path.insert(0, os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..')))
    from craftxpy.memory import (
        StorageManager,
        StorageConfig,
        recommend_storage_config,
        JSONStorage,
        SQLiteStorage,
        HybridStorage
    )

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def demo_json_storage():
    """Demonstrate JSON file storage."""
    print("🗂️  JSON Storage Demo")
    print("=" * 50)

    # Create JSON storage
    json_storage = JSONStorage("demo_logs")

    # Save some conversations
    session_id = f"json_demo_{int(time.time())}"
    json_storage.save_conversation(session_id, "Hello, JSON storage!", "user")
    json_storage.save_conversation(
        session_id, "Hello! I'm using JSON storage.", "assistant")
    json_storage.save_conversation(
        session_id, "How does it work?", "user", {"source": "demo"})

    # Load and display
    history = json_storage.load_conversation(session_id)
    print(f"✅ Stored {len(history)} messages")

    for msg in history:
        print(f"  [{msg['role']}] {msg['message']}")

    # List sessions
    sessions = json_storage.list_sessions()
    print(f"📋 Available sessions: {len(sessions)}")

    print()


def demo_sqlite_storage():
    """Demonstrate SQLite database storage."""
    print("🗄️  SQLite Storage Demo")
    print("=" * 50)

    # Create SQLite storage
    sqlite_storage = SQLiteStorage("demo.db")

    # Save some conversations
    session_id = f"sqlite_demo_{int(time.time())}"
    sqlite_storage.save_conversation(
        session_id, "Hello, SQLite storage!", "user")
    sqlite_storage.save_conversation(
        session_id, "Hello! I'm using SQLite storage.", "assistant")
    sqlite_storage.save_conversation(
        session_id, "This is more scalable!", "user", {"database": "sqlite"})

    # Load and display
    history = sqlite_storage.load_conversation(session_id)
    print(f"✅ Stored {len(history)} messages")

    for msg in history:
        print(f"  [{msg['role']}] {msg['message']}")
        if msg.get('metadata'):
            print(f"    Metadata: {msg['metadata']}")

    # List sessions
    sessions = sqlite_storage.list_sessions()
    print(f"📋 Available sessions: {len(sessions)}")

    print()


def demo_hybrid_storage():
    """Demonstrate hybrid storage system."""
    print("🔄 Hybrid Storage Demo")
    print("=" * 50)

    # Create hybrid storage (SQLite primary, JSON backup)
    primary = SQLiteStorage("hybrid_primary.db")
    secondary = [JSONStorage("hybrid_backup")]
    hybrid_storage = HybridStorage(primary, secondary)

    # Save some conversations
    session_id = f"hybrid_demo_{int(time.time())}"
    hybrid_storage.save_conversation(
        session_id, "Hello, hybrid storage!", "user")
    hybrid_storage.save_conversation(
        session_id, "I'm stored in both SQLite and JSON!", "assistant")
    hybrid_storage.save_conversation(
        session_id,
        "Best of both worlds!",
        "user",
        {"redundancy": "enabled"}
    )

    # Load and display
    history = hybrid_storage.load_conversation(session_id)
    print(f"✅ Stored {len(history)} messages in hybrid system")

    for msg in history:
        print(f"  [{msg['role']}] {msg['message']}")

    # List sessions
    sessions = hybrid_storage.list_sessions()
    print(f"📋 Available sessions: {len(sessions)}")

    print()


def demo_storage_manager():
    """Demonstrate the storage manager with different configurations."""
    print("⚙️  Storage Manager Demo")
    print("=" * 50)

    # Show available profiles
    profiles = StorageConfig.list_profiles()
    print("Available storage profiles:")
    for name, description in profiles.items():
        print(f"  • {name}: {description}")

    print()

    # Test different configurations
    for profile_name in ["development", "production_sqlite"]:
        print(f"Testing {profile_name} profile:")

        config = StorageConfig.get_config(profile_name)
        storage_manager = StorageManager(config)

        session_id = f"{profile_name}_demo_{int(time.time())}"
        storage_manager.save_conversation(
            session_id, f"Hello from {profile_name}!", "user")
        storage_manager.save_conversation(
            session_id,
            f"Hello! Using {profile_name} configuration.",
            "assistant"
        )

        history = storage_manager.load_conversation(session_id)
        print(f"  ✅ {len(history)} messages stored using {profile_name}")
        print()


def demo_storage_recommendations():
    """Demonstrate storage recommendations based on project size."""
    print("💡 Storage Recommendations")
    print("=" * 50)

    project_sizes = ["small_project", "medium_project",
                     "large_project", "enterprise"]

    for size in project_sizes:
        recommendation = recommend_storage_config(size)
        req = recommendation["requirements"]

        print(f"📊 {size.replace('_', ' ').title()}:")
        print(f"  Recommended: {recommendation['profile']}")
        print(f"  Max sessions: {req['max_sessions']}")
        print(f"  Max messages per session: {req['max_messages_per_session']}")
        print(f"  Storage estimate: {req['storage_estimate']}")

        if "additional_features" in req:
            features = ', '.join(req['additional_features'])
            print(f"  Additional features: {features}")

        print()


def performance_comparison():
    """Compare performance of different storage backends."""
    print("🏎️  Performance Comparison")
    print("=" * 50)

    # Test data
    num_messages = 100
    session_id = f"perf_test_{int(time.time())}"

    # JSON Storage
    print("Testing JSON storage...")
    json_storage = JSONStorage("perf_json")
    start_time = time.time()

    for i in range(num_messages):
        json_storage.save_conversation(session_id, f"Message {i}", "user")

    json_time = time.time() - start_time
    print(f"  JSON: {json_time:.3f}s for {num_messages} messages")

    # SQLite Storage
    print("Testing SQLite storage...")
    sqlite_storage = SQLiteStorage("perf_test.db")
    start_time = time.time()

    for i in range(num_messages):
        sqlite_storage.save_conversation(session_id, f"Message {i}", "user")

    sqlite_time = time.time() - start_time
    print(f"  SQLite: {sqlite_time:.3f}s for {num_messages} messages")

    # Performance summary
    print("\n📈 Performance Summary:")
    if sqlite_time > 0:
        speedup = json_time / sqlite_time
        print(f"  SQLite is {speedup:.1f}x faster than JSON for writes")
    else:
        print("  SQLite completed too quickly to measure accurately")

    print()


def cleanup_demo_files():
    """Clean up demo files created during testing."""
    print("🧹 Cleaning up demo files...")

    demo_files = [
        "demo.db", "hybrid_primary.db", "perf_test.db",
        "craftx_production.db", "craftx_primary.db", "craftx.db"
    ]

    demo_dirs = [
        "demo_logs", "hybrid_backup", "perf_json",
        "chat_logs_backup", "local_backup"
    ]

    for file in demo_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"  Removed {file}")
            except OSError as e:
                print(f"  Failed to remove {file}: {e}")

    for dir_name in demo_dirs:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"  Removed {dir_name}/")
            except OSError as e:
                print(f"  Failed to remove {dir_name}/: {e}")

    print("✅ Cleanup completed")


def main():
    """Run all storage system demonstrations."""
    print("🚀 CraftX.py Storage System Demonstrations")
    print("=" * 60)
    print()

    try:
        # Run demonstrations
        demo_json_storage()
        demo_sqlite_storage()
        demo_hybrid_storage()
        demo_storage_manager()
        demo_storage_recommendations()
        performance_comparison()

        print("✨ All demonstrations completed successfully!")
        print()

        # Ask if user wants to clean up
        response = input("Clean up demo files? (y/n): ").lower().strip()
        if response == 'y':
            cleanup_demo_files()

    except (OSError, IOError, ValueError) as e:
        print(f"❌ Error during demonstration: {e}")
        traceback.print_exc()  # Now using the imported traceback module
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    # Removed overly broad exception handler to avoid catching too general exception


if __name__ == "__main__":
    main()
