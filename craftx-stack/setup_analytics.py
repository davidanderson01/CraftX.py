#!/usr/bin/env python3
"""
Analytics Setup Script for CraftX
Installs dependencies and initializes the analytics database
"""

import subprocess
import sys
import os
from pathlib import Path


def install_requirements():
    """Install analytics requirements"""
    print("📦 Installing analytics dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "geoip2>=4.6.0",
            "user-agents>=2.2.0"
        ])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    return True


def download_geoip_database():
    """Download GeoLite2 database (optional)"""
    print("\n🌍 Setting up GeoIP database...")
    print("For IP geolocation, you can download the free GeoLite2 database:")
    print("1. Sign up at https://dev.maxmind.com/geoip/geolite2-free-geolocation-data")
    print("2. Download GeoLite2-City.mmdb")
    print("3. Place it in the craftx-stack directory")
    print("⚠️  Note: This is optional - analytics will work without it")


def initialize_database():
    """Initialize the analytics database"""
    print("\n🗄️  Initializing analytics database...")
    try:
        from user_analytics import analytics
        # The database will be created automatically when first accessed
        print("✅ Analytics database initialized")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        return False


def test_analytics():
    """Test analytics functionality"""
    print("\n🧪 Testing analytics system...")
    try:
        from user_analytics import analytics

        # Test event tracking
        event_id = analytics.track_auth_event(
            provider="test",
            event_type="test_event",
            ip_address="127.0.0.1",
            user_agent="Analytics Setup Script",
            success=True,
            metadata={"test": True}
        )

        # Test summary generation
        summary = analytics.get_analytics_summary(days=1)

        print(f"✅ Analytics test successful")
        print(f"   - Event tracked: {event_id[:8]}...")
        print(
            f"   - Summary generated with {summary['summary']['total_users']} users")
        return True
    except Exception as e:
        print(f"❌ Analytics test failed: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 CraftX Analytics Setup")
    print("=" * 40)

    # Check if we're in the right directory
    if not os.path.exists("craftx.py"):
        print("❌ Please run this script from the craftx-stack directory")
        sys.exit(1)

    # Install requirements
    if not install_requirements():
        sys.exit(1)

    # Download GeoIP info
    download_geoip_database()

    # Initialize database
    if not initialize_database():
        sys.exit(1)

    # Test analytics
    if not test_analytics():
        sys.exit(1)

    print("\n🎉 Analytics setup complete!")
    print("\nNext steps:")
    print("1. Start your CraftX server: python craftx.py")
    print("2. Visit http://localhost:8000/admin/analytics for the dashboard")
    print("3. Test OAuth authentication to generate analytics data")
    print("\nAnalytics features:")
    print("• 👥 User registration and authentication tracking")
    print("• 📊 Real-time dashboard with charts and statistics")
    print("• 🌍 Geographic distribution (with GeoIP database)")
    print("• 📱 Device and browser analytics")
    print("• 📈 Download tracking and user engagement metrics")
    print("• 💾 SQLite database for easy data management")
    print("• 📋 Export functionality for data analysis")


if __name__ == "__main__":
    main()
