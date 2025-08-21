"""
Custom Analytics System for CraftX.py
Independent telemetry and insights without Microsoft/Azure dependencies
"""

import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib
import sqlite3
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class AnalyticsEvent:
    """Custom analytics event structure"""
    event_id: str
    timestamp: str
    event_type: str
    user_id: str
    session_id: str
    properties: Dict[str, Any]
    source: str = "craftx_py"
    version: str = "0.2.0"


class CustomAnalytics:
    """
    Privacy-focused analytics system for CraftX.py
    Stores data locally with optional self-hosted export
    """

    def __init__(self, db_path: str = "craftx_analytics.db", enable_collection: bool = True):
        self.db_path = Path(db_path)
        self.enable_collection = enable_collection
        self.session_id = str(uuid.uuid4())
        self.user_id = self._get_or_create_user_id()

        if self.enable_collection:
            self._init_database()

    def _get_or_create_user_id(self) -> str:
        """Generate anonymous user ID based on system characteristics"""
        import platform
        system_info = f"{platform.system()}-{platform.machine()}-{platform.python_version()}"
        return hashlib.sha256(system_info.encode()).hexdigest()[:16]

    def _init_database(self):
        """Initialize SQLite database for analytics storage"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analytics_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT UNIQUE,
                    timestamp TEXT,
                    event_type TEXT,
                    user_id TEXT,
                    session_id TEXT,
                    properties TEXT,
                    source TEXT,
                    version TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_event_type ON analytics_events(event_type)
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON analytics_events(timestamp)
            """)

    def track_event(self, event_type: str, properties: Dict[str, Any] = None) -> bool:
        """Track a custom event"""
        if not self.enable_collection:
            return False

        event = AnalyticsEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=event_type,
            user_id=self.user_id,
            session_id=self.session_id,
            properties=properties or {}
        )

        return self._store_event(event)

    def _store_event(self, event: AnalyticsEvent) -> bool:
        """Store event in local database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR IGNORE INTO analytics_events 
                    (event_id, timestamp, event_type, user_id, session_id, properties, source, version)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    event.event_id,
                    event.timestamp,
                    event.event_type,
                    event.user_id,
                    event.session_id,
                    json.dumps(event.properties),
                    event.source,
                    event.version
                ))
            return True
        except Exception as e:
            print(f"Analytics storage error: {e}")
            return False

    # Event tracking methods for common CraftX.py activities
    def track_app_start(self, framework_version: str = None):
        """Track application startup"""
        self.track_event("app_start", {
            "framework_version": framework_version or "0.2.0",
            "python_version": self._get_python_version()
        })

    def track_oauth_attempt(self, provider: str, success: bool = False):
        """Track OAuth authentication attempts"""
        self.track_event("oauth_authentication", {
            "provider": provider,
            "success": success,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    def track_webauthn_usage(self, action: str, success: bool = False):
        """Track WebAuthn/passkey usage"""
        self.track_event("webauthn_action", {
            "action": action,  # "register", "authenticate"
            "success": success
        })

    def track_plugin_usage(self, plugin_name: str, action: str = "used"):
        """Track plugin usage"""
        self.track_event("plugin_activity", {
            "plugin_name": plugin_name,
            "action": action
        })

    def track_ai_model_usage(self, model_name: str, tokens_used: int = None):
        """Track AI model usage"""
        self.track_event("ai_model_usage", {
            "model_name": model_name,
            "tokens_used": tokens_used
        })

    def track_error(self, error_type: str, error_message: str = None):
        """Track errors for debugging"""
        self.track_event("error_occurred", {
            "error_type": error_type,
            "error_message": error_message,
            "severity": "error"
        })

    def _get_python_version(self) -> str:
        """Get Python version info"""
        import sys
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    def get_analytics_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get analytics summary for the last N days"""
        if not self.enable_collection:
            return {"error": "Analytics collection disabled"}

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Get event counts by type
                cursor.execute("""
                    SELECT event_type, COUNT(*) as count
                    FROM analytics_events 
                    WHERE timestamp > datetime('now', '-{} days')
                    GROUP BY event_type
                    ORDER BY count DESC
                """.format(days))

                event_counts = dict(cursor.fetchall())

                # Get total events
                cursor.execute("""
                    SELECT COUNT(*) FROM analytics_events 
                    WHERE timestamp > datetime('now', '-{} days')
                """.format(days))

                total_events = cursor.fetchone()[0]

                # Get unique sessions
                cursor.execute("""
                    SELECT COUNT(DISTINCT session_id) FROM analytics_events 
                    WHERE timestamp > datetime('now', '-{} days')
                """.format(days))

                unique_sessions = cursor.fetchone()[0]

                return {
                    "summary_period_days": days,
                    "total_events": total_events,
                    "unique_sessions": unique_sessions,
                    "event_breakdown": event_counts,
                    "generated_at": datetime.now(timezone.utc).isoformat()
                }

        except Exception as e:
            return {"error": f"Failed to generate summary: {e}"}

    def export_data(self, format: str = "json") -> str:
        """Export analytics data"""
        if not self.enable_collection:
            return "{}"

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM analytics_events ORDER BY timestamp DESC")

                columns = [description[0]
                           for description in cursor.description]
                rows = cursor.fetchall()

                data = [dict(zip(columns, row)) for row in rows]

                if format == "json":
                    return json.dumps(data, indent=2)
                else:
                    return str(data)

        except Exception as e:
            return f"Export error: {e}"

    def clear_data(self, confirm: bool = False) -> bool:
        """Clear all analytics data (requires confirmation)"""
        if not confirm:
            print("⚠️  Use clear_data(confirm=True) to actually clear data")
            return False

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("DELETE FROM analytics_events")
            print("✅ Analytics data cleared")
            return True
        except Exception as e:
            print(f"❌ Failed to clear data: {e}")
            return False


# Global analytics instance
_analytics = None


def get_analytics(enable: bool = True) -> CustomAnalytics:
    """Get global analytics instance"""
    global _analytics
    if _analytics is None:
        _analytics = CustomAnalytics(enable_collection=enable)
    return _analytics


def track_event(event_type: str, properties: Dict[str, Any] = None) -> bool:
    """Convenience function for tracking events"""
    return get_analytics().track_event(event_type, properties)

# Privacy-focused configuration


class AnalyticsConfig:
    """Configuration for analytics collection"""

    @staticmethod
    def disable_all_telemetry():
        """Completely disable analytics collection"""
        global _analytics
        _analytics = CustomAnalytics(enable_collection=False)
        print("🔒 All telemetry disabled")

    @staticmethod
    def enable_minimal_analytics():
        """Enable only essential analytics"""
        global _analytics
        _analytics = CustomAnalytics(enable_collection=True)
        print("📊 Minimal analytics enabled (local storage only)")

    @staticmethod
    def show_privacy_info():
        """Show privacy information"""
        print("""
🔒 CraftX.py Custom Analytics - Privacy Information

✅ What we collect (locally):
  - Application usage events (start/stop)
  - OAuth authentication attempts (success/failure)
  - Plugin usage statistics
  - Error occurrences for debugging

❌ What we DON'T collect:
  - Personal information
  - File contents or code
  - Network traffic
  - External API calls

🏠 Data storage:
  - Everything stored locally in SQLite
  - No data sent to external servers
  - You control your data completely

🎛️ Controls:
  - analytics.disable_all_telemetry() - Turn off completely
  - analytics.clear_data(confirm=True) - Delete all data
  - analytics.export_data() - Export your data
        """)


if __name__ == "__main__":
    # Example usage
    analytics = CustomAnalytics()

    # Track some events
    analytics.track_app_start("0.2.0")
    analytics.track_oauth_attempt("github", success=True)
    analytics.track_plugin_usage("dns_validator")

    # Get summary
    summary = analytics.get_analytics_summary()
    print("Analytics Summary:")
    print(json.dumps(summary, indent=2))

    # Show privacy info
    AnalyticsConfig.show_privacy_info()
