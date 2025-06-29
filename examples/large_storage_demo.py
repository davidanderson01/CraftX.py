"""
Example: Managing 1TB+ File Storage with CraftX.py

This example demonstrates how CraftX.py can effectively manage 
terabyte-scale file storage systems.
"""

import os
import sys
import time
import traceback
# Remove unused datetime import

try:
    from craftxpy.plugins.tools.large_storage_manager import LargeStorageManager
    from craftxpy.plugins.tools.file_hydration import FileHydrationMonitor
except ImportError as e:
    print("❌ Required CraftX.py plugins are missing or not installed.")
    print(f"Import error: {e}")
    sys.exit(1)

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def demo_large_storage_capabilities():
    """Demonstrate large storage management capabilities."""
    print("🗄️ CraftX.py Large Storage Management Demo")
    print("=" * 60)
    print("This demo shows how CraftX.py can manage 1TB+ storage systems\n")

    # Initialize large storage manager
    storage_manager = LargeStorageManager(
        database_path="large_storage_demo.db")

    # Example directory (use your actual large directory)
    test_directory = input(
        "Enter a directory to analyze (or press Enter for current): ").strip()
    if not test_directory:
        test_directory = "."

    if not os.path.exists(test_directory):
        print(f"❌ Directory not found: {test_directory}")
        return

    print(f"\n🔍 Analyzing: {test_directory}")
    print("This may take some time for large directories...\n")

    # Perform efficient large-scale scan
    scan_start = time.time()
    progress_count = 0

    for progress in storage_manager.scan_storage_efficient(test_directory):
        progress_count += 1

        if progress["status"] == "counting":
            print(f"📊 {progress['message']}")

        elif progress["status"] == "counted":
            total_files = progress["total_files"]
            print(f"📁 Found {total_files:,} files to analyze\n")

        elif progress["status"] == "scanning":
            if progress_count % 10 == 0:  # Show progress every 10 updates
                print(f"  📁 Processed: {progress['files_processed']:,} files")
                print(f"  💾 Total size: {progress['total_size_gb']:.1f} GB")
                print(f"  💧 Hydrated: {progress['hydrated_percentage']:.1f}%")
                print(
                    f"  📂 Current: {os.path.basename(progress['current_directory'])}")
                print()

        elif progress["status"] == "completed":
            scan_duration = time.time() - scan_start
            print("✅ Scan completed!")
            print("📊 Final Results:")
            print(f"  📁 Total files: {progress['total_files']:,}")
            print(f"  💾 Total size: {progress['total_size_gb']:.1f} GB")
            print(f"  💧 Hydrated files: {progress['hydrated_files']:,}")
            print(f"  💧 Hydrated size: {progress['hydrated_size_gb']:.1f} GB")
            print(f"  ⏱️ Scan duration: {scan_duration:.1f} seconds")
            print(
                f"  🚀 Processing speed: {progress['files_per_second']:.0f} files/second")
            break

        elif progress["status"] == "error":
            print(f"❌ Error: {progress['message']}")
            return

    # Show detailed statistics
    print("\n📊 Detailed Storage Statistics:")
    print("=" * 40)

    stats = storage_manager.get_storage_statistics()

    if stats["overall"]:
        overall = stats["overall"]
        print(f"📁 Files: {overall.get('total_files', 0):,}")
        print(f"💾 Size: {format_size(overall.get('total_size', 0))}")
        print(f"💧 Hydrated: {overall.get('hydrated_files', 0):,} files")
        print(
            f"📊 Average file size: {format_size(overall.get('avg_file_size', 0))}")

    # File type breakdown
    if stats["file_types"]:
        print("\n📋 Top File Types by Size:")
        for i, ft in enumerate(stats["file_types"][:10], 1):
            extension = ft["file_type"] or "No extension"
            size_str = format_size(ft["total_size"])
            print(
                f"  {i:2d}. {extension:12} - {ft['count']:,} files ({size_str})")

    # Directory breakdown
    if stats["top_directories"]:
        print("\n📂 Largest Directories:")
        for i, dir_info in enumerate(stats["top_directories"][:10], 1):
            dir_name = os.path.basename(
                dir_info["directory"]) or dir_info["directory"]
            size_str = format_size(dir_info["total_size"])
            hydrated_str = format_size(dir_info["hydrated_size"])
            print(
                f"  {i:2d}. {dir_name[:30]:30} - {size_str} ({hydrated_str} hydrated)")

    # Find large files
    print("\n🐘 Large Files (>100MB):")
    large_files = storage_manager.find_large_files(min_size_gb=0.1, limit=10)
    if large_files:
        for i, lf in enumerate(large_files, 1):
            hydration_status = "💧" if lf["is_hydrated"] else "❄️"
            file_name = os.path.basename(lf["path"])
            print(
                f"  {i:2d}. {hydration_status} {lf['size_gb']:.1f} GB - {file_name}")
    else:
        print("  No large files found")

    # Hydration report
    print("\n💧 Hydration Analysis:")
    hydration_report = storage_manager.get_hydration_report()

    if hydration_report["overall"]:
        overall = hydration_report["overall"]
        print(f"  Overall hydration: {overall['hydration_percentage']:.1f}%")
        hydrated_size = overall['hydrated_size_gb']
        total_size = overall['total_size_gb']
        print(f"  Hydrated size: {hydrated_size:.1f} GB / {total_size:.1f} GB")

    # Large dehydrated files
    if hydration_report["large_dehydrated_files"]:
        print("\n❄️ Large Dehydrated Files (>100MB):")
        for i, df in enumerate(hydration_report["large_dehydrated_files"][:5], 1):
            file_name = os.path.basename(df["path"])
            print(f"  {i:2d}. {df['size_gb']:.1f} GB - {file_name}")

    # Potential duplicates
    print("\n🔄 Potential Duplicate Files:")
    duplicates = storage_manager.find_duplicate_files(min_size_mb=10)
    if duplicates:
        for i, dup in enumerate(duplicates[:5], 1):
            print(
                f"  {i:2d}. {dup['size_mb']:.1f} MB - {dup['file_count']} files with same size")
    else:
        print("  No potential duplicates found")

    print("\n🎯 Storage Management Recommendations:")

    # Generate recommendations based on analysis
    if hydration_report["overall"]:
        hydration_pct = hydration_report["overall"]["hydration_percentage"]

        if hydration_pct < 50:
            print("  ⚠️ Low hydration detected. Consider:")
            print("     - Hydrating frequently accessed files")
            print("     - Reviewing OneDrive sync settings")
            print("     - Prioritizing critical files for local storage")
        elif hydration_pct < 80:
            print("  📊 Moderate hydration. Consider:")
            print("     - Selective hydration of important files")
            print("     - Regular hydration monitoring")
        else:
            print("  ✅ Good hydration levels maintained")

    if large_files and len(large_files) > 10:
        print("  📁 Many large files detected. Consider:")
        print("     - Archive old large files")
        print("     - Compress media files")
        print("     - Move infrequently accessed files to cold storage")

    if duplicates and len(duplicates) > 5:
        print("  🔄 Potential duplicates found. Consider:")
        print("     - Running duplicate file cleanup")
        print("     - Implementing deduplication strategy")

    print("\n💡 Next Steps:")
    print("  1. Set up regular automated scans")
    print("  2. Monitor hydration status of critical files")
    print("  3. Implement tiered storage strategy")
    print("  4. Consider cloud archival for old files")


def demo_enhanced_hydration_tool():
    """Demonstrate enhanced hydration monitoring for large storage."""
    print("\n💧 Enhanced Hydration Monitoring Demo")
    print("=" * 50)

    monitor = FileHydrationMonitor()

    test_directory = input("Enter directory for hydration analysis: ").strip()
    if not test_directory or not os.path.exists(test_directory):
        print("Using current directory for demo")
        test_directory = "."

    print("\n🔍 Basic Hydration Check:")
    basic_result = monitor.run(path=test_directory)
    print(basic_result)

    print("\n🔍 Enhanced Hydration Check (1000 files):")
    enhanced_result = monitor.run(
        path=test_directory,
        max_files=1000,
        deep_scan=True
    )
    print(enhanced_result)

    print("\n🚀 Large-Scale Hydration Analysis:")
    large_scale_result = monitor.run(
        path=test_directory,
        max_files=10000,
        large_scale=True
    )
    print(large_scale_result)


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"

    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def main():
    """Run the large storage management demonstration."""
    print("🗄️ CraftX.py - Large Storage Management Capabilities")
    print("=" * 65)
    print("This demonstration shows how CraftX.py can effectively")
    print("manage and analyze terabyte-scale file storage systems.")
    print()

    choice = input(
        "Choose demo: (1) Large Storage Analysis, (2) Enhanced Hydration, (3) Both: ").strip()

    try:
        if choice in ["1", "3"]:
            demo_large_storage_capabilities()

        if choice in ["2", "3"]:
            demo_enhanced_hydration_tool()

        print("\n✨ Demo completed!")
        print("\n🎯 Key Capabilities for 1TB+ Storage:")
        print("  ✅ Efficient scanning of millions of files")
        print("  ✅ Real-time progress tracking")
        print("  ✅ Detailed storage analytics and reporting")
        print("  ✅ Hydration status monitoring")
        print("  ✅ Large file identification")
        print("  ✅ Duplicate file detection")
        print("  ✅ Scalable database indexing")
        print("  ✅ Intelligent sampling for performance")
        print("  ✅ Comprehensive storage recommendations")

        # Cleanup
        cleanup = input("\nClean up demo database? (y/n): ").lower().strip()
        if cleanup == 'y':
            demo_files = ["large_storage_demo.db"]
            for file in demo_files:
                if os.path.exists(file):
                    os.remove(file)
                    print(f"  Removed {file}")
            print("✅ Cleanup completed")

    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
        print(f"\n❌ Error during demo: {e}")
        traceback.print_exc()
        traceback.print_exc()


if __name__ == "__main__":
    main()
