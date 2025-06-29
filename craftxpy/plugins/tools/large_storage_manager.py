"""
Large-scale file storage management for CraftX.py

This module provides tools for managing terabyte-scale file storage,
including efficient scanning, indexing, and batch operations.
"""

import os
import time
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Generator, Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class FileInfo:
    """Information about a file in the storage system."""
    path: str
    size: int
    modified_time: float
    created_time: float
    is_hydrated: bool
    file_hash: Optional[str] = None
    file_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class LargeStorageManager:
    """Manager for large-scale file storage operations."""

    def __init__(self, database_path: str = "file_storage.db", max_workers: int = 4):
        self.database_path = database_path
        self.max_workers = max_workers
        self._stop_scan = False
        self._last_progress = None
        self.init_database()

    def init_database(self):
        """Initialize the file index database."""
        with sqlite3.connect(self.database_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE NOT NULL,
                    filename TEXT NOT NULL,
                    directory TEXT NOT NULL,
                    size INTEGER NOT NULL,
                    modified_time REAL NOT NULL,
                    created_time REAL NOT NULL,
                    is_hydrated BOOLEAN NOT NULL,
                    file_hash TEXT,
                    file_type TEXT,
                    scan_time REAL NOT NULL,
                    metadata JSON
                )
            """)

            # Create indexes for performance
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_files_path ON files(path)")
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_files_directory ON files(directory)")
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_files_size ON files(size)")
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_files_modified ON files(modified_time)")
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_files_hydrated ON files(is_hydrated)")

            # Storage summary table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS storage_summary (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_time REAL NOT NULL,
                    total_files INTEGER NOT NULL,
                    total_size INTEGER NOT NULL,
                    hydrated_files INTEGER NOT NULL,
                    hydrated_size INTEGER NOT NULL,
                    scan_duration REAL NOT NULL,
                    root_path TEXT NOT NULL
                )
            """)

    def scan_storage_efficient(self, scan_root_path: str,
                               progress_callback=None,
                               batch_size: int = 1000) -> Generator[Dict[str, Any], None, None]:
        """
        Efficiently scan large storage volumes with progress tracking.

        Args:
            scan_root_path: Root directory to scan
            progress_callback: Function to call with progress updates
            batch_size: Number of files to process in each batch

        Yields:
            Progress updates and statistics
        """
        scan_start = time.time()
        # Scanning statistics
        scan_stats = {
            'total_files': 0,
            'total_size': 0,
            'hydrated_files': 0,
            'hydrated_size': 0
        }
        batch_files = []

        self._stop_scan = False

        try:
            # First pass: count total files for progress tracking
            if progress_callback:
                yield {"status": "counting", "message": "Counting files..."}
                file_count = sum(1 for _, _, files in os.walk(scan_root_path)
                                 for _ in files)
                yield {"status": "counted", "total_files": file_count}

            # Main scanning loop
            for root, dirs, files in os.walk(scan_root_path):
                if self._stop_scan:
                    break

                # Skip system and hidden directories for performance
                dirs[:] = [d for d in dirs if not d.startswith(
                    '.') and d not in ['$RECYCLE.BIN', 'System Volume Information']]

                batch_files = self._process_directory_files(
                    root, files, scan_stats, batch_files, batch_size, progress_callback
                )
                # Yield any progress updates
                if hasattr(self, '_last_progress') and self._last_progress:
                    yield self._last_progress
                    self._last_progress = None

            # Process remaining files
            if batch_files:
                self._save_file_batch(batch_files)

            # Save summary and yield final results
            yield from self._finalize_scan(scan_start, scan_stats, scan_root_path)

        except (OSError, PermissionError, IOError) as e:
            yield {"status": "error", "message": str(e)}

    def _process_directory_files(self, root: str, files: List[str], scan_stats: Dict[str, int],
                                 batch_files: List[FileInfo], batch_size: int,
                                 progress_callback) -> List[FileInfo]:
        """Process all files in a directory."""
        for filename in files:
            if self._stop_scan:
                break

            file_path = os.path.join(root, filename)
            file_info = self._process_file(file_path, scan_stats)

            if file_info:
                batch_files.append(file_info)
                batch_files = self._process_batch_if_ready(
                    batch_files, batch_size, scan_stats, root, progress_callback
                )
        return batch_files

    def _finalize_scan(self, scan_start: float, scan_stats: Dict[str, int],
                       scan_root_path: str) -> Generator[Dict[str, Any], None, None]:
        """Finalize scan and yield results."""
        scan_duration = time.time() - scan_start
        summary_data = {
            'scan_time': scan_start,
            'total_files': scan_stats['total_files'],
            'total_size': scan_stats['total_size'],
            'hydrated_files': scan_stats['hydrated_files'],
            'hydrated_size': scan_stats['hydrated_size'],
            'scan_duration': scan_duration,
            'root_path': scan_root_path
        }
        self._save_scan_summary(summary_data)

        yield {
            "status": "completed",
            "total_files": scan_stats['total_files'],
            "total_size_gb": scan_stats['total_size'] / (1024**3),
            "hydrated_files": scan_stats['hydrated_files'],
            "hydrated_size_gb": scan_stats['hydrated_size'] / (1024**3),
            "scan_duration": scan_duration,
            "files_per_second": (
                scan_stats['total_files'] /
                scan_duration if scan_duration > 0 else 0
            )
        }

    def _get_file_info(self, file_path: str) -> Optional[FileInfo]:
        """Get comprehensive information about a file."""
        try:
            stat = os.stat(file_path)

            # Check hydration status (Windows OneDrive)
            is_hydrated = True
            if hasattr(stat, 'st_file_attributes'):
                attributes = stat.st_file_attributes
                is_hydrated = not attributes & 0x400000  # Not a placeholder
            else:
                is_hydrated = stat.st_size > 0

            return FileInfo(
                path=file_path,
                size=stat.st_size,
                modified_time=stat.st_mtime,
                created_time=stat.st_ctime,
                is_hydrated=is_hydrated,
                file_type=Path(file_path).suffix.lower()
            )

        except (OSError, PermissionError):
            return None

    def _save_file_batch(self, files: List[FileInfo]):
        """Save a batch of files to the database."""
        with sqlite3.connect(self.database_path) as conn:
            conn.executemany("""
                INSERT OR REPLACE INTO files 
                (path, filename, directory, size, modified_time, created_time, 
                 is_hydrated, file_type, scan_time, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                (
                    file_info.path,
                    os.path.basename(file_info.path),
                    os.path.dirname(file_info.path),
                    file_info.size,
                    file_info.modified_time,
                    file_info.created_time,
                    file_info.is_hydrated,
                    file_info.file_type,
                    time.time(),
                    None  # metadata as JSON
                )
                for file_info in files
            ])

    def _save_scan_summary(self, summary_data: Dict[str, Any]):
        """Save scan summary to database."""
        with sqlite3.connect(self.database_path) as conn:
            conn.execute("""
                INSERT INTO storage_summary 
                (scan_time, total_files, total_size, hydrated_files, hydrated_size, 
                 scan_duration, root_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                summary_data['scan_time'],
                summary_data['total_files'],
                summary_data['total_size'],
                summary_data['hydrated_files'],
                summary_data['hydrated_size'],
                summary_data['scan_duration'],
                summary_data['root_path']
            ))

    def get_storage_statistics(self) -> Dict[str, Any]:
        """Get comprehensive storage statistics."""
        with sqlite3.connect(self.database_path) as conn:
            conn.row_factory = sqlite3.Row

            # Overall statistics
            overall_stats = conn.execute("""
                SELECT 
                    COUNT(*) as total_files,
                    SUM(size) as total_size,
                    SUM(CASE WHEN is_hydrated THEN 1 ELSE 0 END) as hydrated_files,
                    SUM(CASE WHEN is_hydrated THEN size ELSE 0 END) as hydrated_size,
                    AVG(size) as avg_file_size,
                    MAX(scan_time) as last_scan_time
                FROM files
            """).fetchone()

            # File type breakdown
            file_types = conn.execute("""
                SELECT 
                    file_type,
                    COUNT(*) as count,
                    SUM(size) as total_size
                FROM files 
                WHERE file_type IS NOT NULL
                GROUP BY file_type
                ORDER BY total_size DESC
                LIMIT 10
            """).fetchall()

            # Directory sizes
            directories = conn.execute("""
                SELECT 
                    directory,
                    COUNT(*) as file_count,
                    SUM(size) as total_size,
                    SUM(CASE WHEN is_hydrated THEN size ELSE 0 END) as hydrated_size
                FROM files
                GROUP BY directory
                ORDER BY total_size DESC
                LIMIT 20
            """).fetchall()

            return {
                "overall": dict(overall_stats) if overall_stats else {},
                "file_types": [dict(row) for row in file_types],
                "top_directories": [dict(row) for row in directories],
                "scan_time": (
                    datetime.fromtimestamp(
                        overall_stats['last_scan_time']).isoformat()
                    if overall_stats and overall_stats['last_scan_time'] else None
                )
            }

    def find_large_files(self, min_size_gb: float = 1.0, limit: int = 100) -> List[Dict[str, Any]]:
        """Find large files above a certain size."""
        min_size_bytes = int(min_size_gb * 1024**3)

        with sqlite3.connect(self.database_path) as conn:
            conn.row_factory = sqlite3.Row

            results = conn.execute("""
                SELECT path, size, is_hydrated, file_type, modified_time
                FROM files
                WHERE size >= ?
                ORDER BY size DESC
                LIMIT ?
            """, (min_size_bytes, limit)).fetchall()

            return [
                {
                    "path": row["path"],
                    "size_gb": row["size"] / (1024**3),
                    "is_hydrated": bool(row["is_hydrated"]),
                    "file_type": row["file_type"],
                    "modified_date": datetime.fromtimestamp(row["modified_time"]).isoformat()
                }
                for row in results
            ]

    def find_duplicate_files(self, min_size_mb: float = 1.0) -> List[Dict[str, Any]]:
        """Find potential duplicate files based on size (requires hash calculation)."""
        min_size_bytes = int(min_size_mb * 1024**2)

        with sqlite3.connect(self.database_path) as conn:
            conn.row_factory = sqlite3.Row

            # Find files with same size
            duplicates = conn.execute("""
                SELECT size, COUNT(*) as count, GROUP_CONCAT(path) as paths
                FROM files
                WHERE size >= ? AND size > 0
                GROUP BY size
                HAVING COUNT(*) > 1
                ORDER BY size DESC
                LIMIT 50
            """, (min_size_bytes,)).fetchall()

            return [
                {
                    "size_mb": row["size"] / (1024**2),
                    "file_count": row["count"],
                    "paths": row["paths"].split(",") if row["paths"] else []
                }
                for row in duplicates
            ]

    def get_hydration_report(self) -> Dict[str, Any]:
        """Get detailed hydration status report."""
        with sqlite3.connect(self.database_path) as conn:
            conn.row_factory = sqlite3.Row

            # Overall hydration status
            hydration_overall = conn.execute("""
                SELECT 
                    COUNT(*) as total_files,
                    SUM(size) as total_size,
                    SUM(CASE WHEN is_hydrated THEN 1 ELSE 0 END) as hydrated_files,
                    SUM(CASE WHEN is_hydrated THEN size ELSE 0 END) as hydrated_size
                FROM files
            """).fetchone()

            # Hydration by directory
            by_directory = conn.execute("""
                SELECT 
                    directory,
                    COUNT(*) as total_files,
                    SUM(CASE WHEN is_hydrated THEN 1 ELSE 0 END) as hydrated_files,
                    SUM(size) as total_size,
                    SUM(CASE WHEN is_hydrated THEN size ELSE 0 END) as hydrated_size
                FROM files
                GROUP BY directory
                HAVING total_files > 10
                ORDER BY total_size DESC
                LIMIT 20
            """).fetchall()

            # Large non-hydrated files
            large_dehydrated = conn.execute("""
                SELECT path, size, file_type
                FROM files
                WHERE is_hydrated = 0 AND size > 100000000  -- > 100MB
                ORDER BY size DESC
                LIMIT 20
            """).fetchall()

            return {
                "overall": {
                    "total_files": hydration_overall["total_files"],
                    "total_size_gb": hydration_overall["total_size"] / (1024**3),
                    "hydrated_files": hydration_overall["hydrated_files"],
                    "hydrated_size_gb": hydration_overall["hydrated_size"] / (1024**3),
                    "hydration_percentage": (
                        hydration_overall["hydrated_files"] /
                        hydration_overall["total_files"] * 100
                    ) if hydration_overall["total_files"] > 0 else 0
                },
                "by_directory": [
                    {
                        "directory": row["directory"],
                        "total_files": row["total_files"],
                        "hydrated_files": row["hydrated_files"],
                        "hydration_percentage": (
                            row["hydrated_files"] / row["total_files"] * 100
                        ) if row["total_files"] > 0 else 0,
                        "total_size_gb": row["total_size"] / (1024**3),
                        "hydrated_size_gb": row["hydrated_size"] / (1024**3)
                    }
                    for row in by_directory
                ],
                "large_dehydrated_files": [
                    {
                        "path": row["path"],
                        "size_gb": row["size"] / (1024**3),
                        "file_type": row["file_type"]
                    }
                    for row in large_dehydrated
                ]
            }

    def stop_scan(self):
        """Stop the current scan operation."""
        self._stop_scan = True

    def cleanup_database(self, days_old: int = 30):
        """Clean up old scan data."""
        cutoff_time = time.time() - (days_old * 24 * 60 * 60)

        with sqlite3.connect(self.database_path) as conn:
            # Remove old file records
            conn.execute("DELETE FROM files WHERE scan_time < ?",
                         (cutoff_time,))

            # Remove old summaries
            conn.execute(
                "DELETE FROM storage_summary WHERE scan_time < ?", (cutoff_time,))

            # Vacuum to reclaim space
            conn.execute("VACUUM")

    def _process_file(self, file_path: str, scan_stats: Dict[str, int]) -> Optional[FileInfo]:
        """Process a single file and update statistics."""
        try:
            file_info = self._get_file_info(file_path)
            if file_info:
                scan_stats['total_files'] += 1
                scan_stats['total_size'] += file_info.size

                if file_info.is_hydrated:
                    scan_stats['hydrated_files'] += 1
                    scan_stats['hydrated_size'] += file_info.size

                return file_info
        except (OSError, PermissionError):
            pass  # Skip inaccessible files
        return None

    def _process_batch_if_ready(self, batch_files: List[FileInfo], batch_size: int,
                                scan_stats: Dict[str, int], current_dir: str,
                                progress_callback) -> List[FileInfo]:
        """Process batch if it's ready and return new empty batch."""
        if len(batch_files) >= batch_size:
            self._save_file_batch(batch_files)

            if progress_callback:
                progress_data = {
                    "status": "scanning",
                    "files_processed": scan_stats['total_files'],
                    "current_directory": current_dir,
                    "total_size_gb": scan_stats['total_size'] / (1024**3),
                    "hydrated_percentage": (
                        scan_stats['hydrated_files'] /
                        scan_stats['total_files'] * 100
                    ) if scan_stats['total_files'] > 0 else 0
                }
                # Store progress data for yielding in main method
                self._last_progress = progress_data

            return []  # Return empty batch
        return batch_files  # Return original batch


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format."""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    if seconds < 3600:
        return f"{seconds/60:.1f} minutes"
    return f"{seconds/3600:.1f} hours"


if __name__ == "__main__":
    # Example usage for large storage management
    storage_manager = LargeStorageManager()

    # Scan a directory
    ROOT_PATH = input("Enter directory to scan: ").strip()
    if not ROOT_PATH:
        ROOT_PATH = "."

    print(f"Scanning {ROOT_PATH}...")

    for progress in storage_manager.scan_storage_efficient(ROOT_PATH):
        if progress["status"] == "scanning":
            print(f"  Processed: {progress['files_processed']} files, "
                  f"Size: {progress['total_size_gb']:.1f} GB, "
                  f"Hydrated: {progress['hydrated_percentage']:.1f}%")
        elif progress["status"] == "completed":
            print("\n✅ Scan completed!")
            print(f"  Total files: {progress['total_files']:,}")
            print(
                f"  Total size: {format_size(int(progress['total_size_gb'] * 1024**3))}")
            print(f"  Hydrated files: {progress['hydrated_files']:,}")
            print(
                f"  Scan duration: {format_duration(progress['scan_duration'])}")
            print(f"  Files per second: {progress['files_per_second']:.0f}")

    # Show statistics
    print("\n📊 Storage Statistics:")
    stats = storage_manager.get_storage_statistics()
    if stats["overall"]:
        overall = stats["overall"]
        print(f"  Files: {overall.get('total_files', 0):,}")
        print(f"  Size: {format_size(overall.get('total_size', 0))}")
        print(f"  Hydrated: {overall.get('hydrated_files', 0):,} files")
        print(
            f"  Average file size: {format_size(overall.get('avg_file_size', 0))}")
