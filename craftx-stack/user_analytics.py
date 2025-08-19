"""
CraftX User Analytics and Tracking System
Tracks user authentication events, demographics, and usage patterns
"""

import json
import os
import sqlite3
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import geoip2.database
import geoip2.errors
from user_agents import parse as parse_user_agent


@dataclass
class UserSession:
    """User session data structure"""
    session_id: str
    user_id: str
    email: Optional[str]
    provider: str
    ip_address: str
    user_agent: str
    country: Optional[str]
    city: Optional[str]
    device_type: str
    browser: str
    os: str
    created_at: str
    last_active: str
    download_count: int = 0
    is_active: bool = True


@dataclass
class AuthEvent:
    """Authentication event data structure"""
    event_id: str
    user_id: str
    provider: str
    event_type: str  # login, logout, register, download, error
    ip_address: str
    user_agent: str
    success: bool
    error_message: Optional[str]
    timestamp: str
    metadata: Dict[str, Any]


class UserAnalytics:
    """User analytics and tracking system"""

    def __init__(self, db_path: str = "user_analytics.db"):
        self.db_path = db_path
        self.geoip_db = None
        self._init_database()
        self._init_geoip()

    def _init_database(self):
        """Initialize SQLite database for user tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                email TEXT,
                provider TEXT NOT NULL,
                first_seen TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                total_logins INTEGER DEFAULT 1,
                total_downloads INTEGER DEFAULT 0,
                country TEXT,
                city TEXT,
                preferred_device TEXT,
                preferred_browser TEXT,
                preferred_os TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                metadata TEXT
            )
        """)

        # Create sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                user_agent TEXT NOT NULL,
                country TEXT,
                city TEXT,
                device_type TEXT,
                browser TEXT,
                os TEXT,
                created_at TEXT NOT NULL,
                last_active TEXT NOT NULL,
                download_count INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)

        # Create auth_events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS auth_events (
                event_id TEXT PRIMARY KEY,
                user_id TEXT,
                provider TEXT NOT NULL,
                event_type TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                user_agent TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                error_message TEXT,
                timestamp TEXT NOT NULL,
                metadata TEXT
            )
        """)

        # Create analytics_summary table for quick stats
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics_summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                total_users INTEGER DEFAULT 0,
                new_users INTEGER DEFAULT 0,
                active_sessions INTEGER DEFAULT 0,
                total_downloads INTEGER DEFAULT 0,
                top_provider TEXT,
                top_country TEXT,
                updated_at TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def _init_geoip(self):
        """Initialize GeoIP database if available"""
        geoip_paths = [
            "GeoLite2-City.mmdb",
            "/usr/share/GeoIP/GeoLite2-City.mmdb",
            "/opt/GeoIP/GeoLite2-City.mmdb"
        ]

        for path in geoip_paths:
            if os.path.exists(path):
                try:
                    self.geoip_db = geoip2.database.Reader(path)
                    print(f"✅ GeoIP database loaded from {path}")
                    break
                except Exception as e:
                    print(f"⚠️  Failed to load GeoIP from {path}: {e}")

    def _get_location(self, ip_address: str) -> tuple[Optional[str], Optional[str]]:
        """Get country and city from IP address"""
        if not self.geoip_db or ip_address in ['127.0.0.1', 'localhost']:
            return None, None

        try:
            response = self.geoip_db.city(ip_address)
            country = response.country.name
            city = response.city.name
            return country, city
        except (geoip2.errors.AddressNotFoundError, Exception):
            return None, None

    def _parse_user_agent(self, user_agent: str) -> tuple[str, str, str]:
        """Parse user agent to extract device, browser, and OS info"""
        try:
            ua = parse_user_agent(user_agent)
            device_type = "mobile" if ua.is_mobile else "tablet" if ua.is_tablet else "desktop"
            browser = f"{ua.browser.family} {ua.browser.version_string}" if ua.browser.family else "Unknown"
            os = f"{ua.os.family} {ua.os.version_string}" if ua.os.family else "Unknown"
            return device_type, browser, os
        except Exception:
            return "unknown", "Unknown", "Unknown"

    def track_auth_event(self, provider: str, event_type: str, ip_address: str,
                         user_agent: str, success: bool = True,
                         error_message: Optional[str] = None,
                         user_id: Optional[str] = None,
                         metadata: Optional[Dict[str, Any]] = None) -> str:
        """Track an authentication event"""
        event_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        event = AuthEvent(
            event_id=event_id,
            user_id=user_id or "anonymous",
            provider=provider,
            event_type=event_type,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            error_message=error_message,
            timestamp=timestamp,
            metadata=metadata or {}
        )

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO auth_events (
                event_id, user_id, provider, event_type, ip_address, user_agent,
                success, error_message, timestamp, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event.event_id, event.user_id, event.provider, event.event_type,
            event.ip_address, event.user_agent, event.success, event.error_message,
            event.timestamp, json.dumps(event.metadata)
        ))

        conn.commit()
        conn.close()

        return event_id

    def create_user_session(self, user_id: str, email: Optional[str], provider: str,
                            ip_address: str, user_agent: str) -> str:
        """Create a new user session and track user data"""
        session_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        # Get location and device info
        country, city = self._get_location(ip_address)
        device_type, browser, os = self._parse_user_agent(user_agent)

        # Create session
        session = UserSession(
            session_id=session_id,
            user_id=user_id,
            email=email,
            provider=provider,
            ip_address=ip_address,
            user_agent=user_agent,
            country=country,
            city=city,
            device_type=device_type,
            browser=browser,
            os=os,
            created_at=timestamp,
            last_active=timestamp
        )

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Insert or update user record
        cursor.execute("""
            INSERT OR REPLACE INTO users (
                user_id, email, provider, first_seen, last_seen, total_logins,
                total_downloads, country, city, preferred_device, preferred_browser,
                preferred_os, is_active, metadata
            ) VALUES (
                ?, ?, ?, 
                COALESCE((SELECT first_seen FROM users WHERE user_id = ?), ?),
                ?,
                COALESCE((SELECT total_logins FROM users WHERE user_id = ?), 0) + 1,
                COALESCE((SELECT total_downloads FROM users WHERE user_id = ?), 0),
                ?, ?, ?, ?, ?, TRUE, ?
            )
        """, (
            user_id, email, provider, user_id, timestamp, timestamp,
            user_id, user_id, country, city, device_type, browser, os,
            json.dumps({})
        ))

        # Insert session record
        cursor.execute("""
            INSERT INTO sessions (
                session_id, user_id, ip_address, user_agent, country, city,
                device_type, browser, os, created_at, last_active, download_count, is_active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, TRUE)
        """, (
            session_id, user_id, ip_address, user_agent, country, city,
            device_type, browser, os, timestamp, timestamp
        ))

        conn.commit()
        conn.close()

        # Track login event
        self.track_auth_event(
            provider=provider,
            event_type="login",
            ip_address=ip_address,
            user_agent=user_agent,
            user_id=user_id,
            metadata={"email": email, "session_id": session_id}
        )

        return session_id

    def track_download(self, user_id: str, session_id: str):
        """Track a download event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Update user download count
        cursor.execute("""
            UPDATE users SET total_downloads = total_downloads + 1,
                            last_seen = ?
            WHERE user_id = ?
        """, (datetime.now().isoformat(), user_id))

        # Update session download count
        cursor.execute("""
            UPDATE sessions SET download_count = download_count + 1,
                              last_active = ?
            WHERE session_id = ?
        """, (datetime.now().isoformat(), session_id))

        conn.commit()
        conn.close()

    def get_analytics_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get analytics summary for the last N days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        since_date = (datetime.now() - timedelta(days=days)).isoformat()

        # Total users
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        # New users in period
        cursor.execute(
            "SELECT COUNT(*) FROM users WHERE first_seen >= ?", (since_date,))
        new_users = cursor.fetchone()[0]

        # Active sessions
        active_since = (datetime.now() - timedelta(hours=24)).isoformat()
        cursor.execute(
            "SELECT COUNT(*) FROM sessions WHERE last_active >= ? AND is_active = TRUE", (active_since,))
        active_sessions = cursor.fetchone()[0]

        # Total downloads
        cursor.execute("SELECT SUM(total_downloads) FROM users")
        total_downloads = cursor.fetchone()[0] or 0

        # Top provider
        cursor.execute("""
            SELECT provider, COUNT(*) as count FROM users 
            GROUP BY provider ORDER BY count DESC LIMIT 1
        """)
        top_provider_result = cursor.fetchone()
        top_provider = top_provider_result[0] if top_provider_result else "none"

        # Top country
        cursor.execute("""
            SELECT country, COUNT(*) as count FROM users 
            WHERE country IS NOT NULL 
            GROUP BY country ORDER BY count DESC LIMIT 1
        """)
        top_country_result = cursor.fetchone()
        top_country = top_country_result[0] if top_country_result else "unknown"

        # Recent activity
        cursor.execute("""
            SELECT DATE(timestamp) as date, COUNT(*) as events
            FROM auth_events 
            WHERE timestamp >= ? AND success = TRUE
            GROUP BY DATE(timestamp)
            ORDER BY date DESC
            LIMIT 7
        """, (since_date,))
        recent_activity = dict(cursor.fetchall())

        # Provider breakdown
        cursor.execute("""
            SELECT provider, COUNT(*) as count FROM users 
            GROUP BY provider ORDER BY count DESC
        """)
        provider_breakdown = dict(cursor.fetchall())

        # Device breakdown
        cursor.execute("""
            SELECT preferred_device, COUNT(*) as count FROM users 
            WHERE preferred_device IS NOT NULL
            GROUP BY preferred_device ORDER BY count DESC
        """)
        device_breakdown = dict(cursor.fetchall())

        conn.close()

        return {
            "summary": {
                "total_users": total_users,
                "new_users": new_users,
                "active_sessions": active_sessions,
                "total_downloads": total_downloads,
                "top_provider": top_provider,
                "top_country": top_country
            },
            "recent_activity": recent_activity,
            "provider_breakdown": provider_breakdown,
            "device_breakdown": device_breakdown,
            "period_days": days,
            "generated_at": datetime.now().isoformat()
        }

    def get_user_details(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get user info
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user_row = cursor.fetchone()

        if not user_row:
            conn.close()
            return None

        # Get user sessions
        cursor.execute("""
            SELECT * FROM sessions WHERE user_id = ? 
            ORDER BY created_at DESC LIMIT 10
        """, (user_id,))
        sessions = cursor.fetchall()

        # Get recent auth events
        cursor.execute("""
            SELECT * FROM auth_events WHERE user_id = ? 
            ORDER BY timestamp DESC LIMIT 20
        """, (user_id,))
        events = cursor.fetchall()

        conn.close()

        return {
            "user": dict(zip([col[0] for col in cursor.description], user_row)),
            "recent_sessions": [dict(zip([col[0] for col in cursor.description], session)) for session in sessions],
            "recent_events": [dict(zip([col[0] for col in cursor.description], event)) for event in events]
        }

    def export_analytics(self, format: str = "json") -> str:
        """Export analytics data in specified format"""
        summary = self.get_analytics_summary(days=90)

        if format.lower() == "json":
            return json.dumps(summary, indent=2)
        elif format.lower() == "csv":
            # Simple CSV export of summary data
            lines = ["metric,value"]
            for key, value in summary["summary"].items():
                lines.append(f"{key},{value}")
            return "\n".join(lines)
        else:
            raise ValueError("Unsupported format. Use 'json' or 'csv'")


# Global analytics instance
analytics = UserAnalytics()
