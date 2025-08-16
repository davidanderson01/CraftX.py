#!/usr/bin/env python3
"""
Test script for CraftX OAuth functionality
"""

import requests
import sys
from pathlib import Path


def test_server_health():
    """Test if the CraftX server is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def test_oauth_status():
    """Test OAuth configuration status"""
    try:
        response = requests.get(
            "http://localhost:8000/admin/oauth-status", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None


def test_oauth_endpoints():
    """Test OAuth endpoints for available providers"""
    status = test_oauth_status()
    if not status or "providers" not in status:
        return []

    working_providers = []
    for provider, config in status["providers"].items():
        if config.get("configured"):
            try:
                # Test the OAuth initiation endpoint (should redirect)
                response = requests.get(f"http://localhost:8000/auth/{provider}",
                                        allow_redirects=False, timeout=5)
                if response.status_code in [302, 307]:  # Redirect response
                    working_providers.append(provider)
            except requests.exceptions.RequestException:
                pass

    return working_providers


def main():
    print("🧪 CraftX OAuth Test Suite")
    print("=" * 40)

    # Test 1: Server Health
    print("\n1. Testing server health...")
    if test_server_health():
        print("   ✅ Server is running and responsive")
    else:
        print("   ❌ Server is not running or not responsive")
        print("   💡 Make sure to start the server with: python craftx.py")
        return 1

    # Test 2: OAuth System
    print("\n2. Testing OAuth system...")
    status = test_oauth_status()
    if status is None:
        print("   ❌ OAuth system is not available")
        return 1
    elif "error" in status:
        print(f"   ❌ OAuth error: {status['error']}")
        return 1
    else:
        total_configured = status.get("total_configured", 0)
        print(
            f"   ✅ OAuth system available ({total_configured} providers configured)")

    # Test 3: Provider Configuration
    print("\n3. Testing provider configurations...")
    providers = status.get("providers", {})
    if not providers:
        print("   ⚠️  No providers found")
        return 1

    configured_providers = []
    for provider, config in providers.items():
        if config.get("configured"):
            status_icon = "✅" if config.get("has_client_id") else "⚠️"
            print(
                f"   {status_icon} {provider}: {'Ready' if config.get('has_client_id') else 'Missing client_id'}")
            if config.get("has_client_id"):
                configured_providers.append(provider)
        else:
            print(f"   ❌ {provider}: Not configured")

    if not configured_providers:
        print("\n   💡 No providers are fully configured. Run: python oauth_setup.py")
        return 1

    # Test 4: OAuth Endpoints
    print("\n4. Testing OAuth endpoints...")
    working_providers = test_oauth_endpoints()

    for provider in configured_providers:
        if provider in working_providers:
            print(f"   ✅ {provider}: OAuth endpoint working")
            print(f"      🔗 Test URL: http://localhost:8000/auth/{provider}")
        else:
            print(f"   ❌ {provider}: OAuth endpoint not working")

    # Summary
    print("\n" + "=" * 40)
    print("📋 Test Summary:")
    print(f"   • Server: {'✅ Running' if test_server_health() else '❌ Down'}")
    print(
        f"   • OAuth System: {'✅ Available' if status and 'error' not in status else '❌ Unavailable'}")
    print(f"   • Configured Providers: {len(configured_providers)}")
    print(f"   • Working Endpoints: {len(working_providers)}")

    if working_providers:
        print(f"\n🎉 OAuth is working! Try these providers:")
        for provider in working_providers:
            print(f"   • {provider}: http://localhost:8000/auth/{provider}")
        print(f"\n🌐 Visit your website: http://localhost:8000")
        return 0
    else:
        print(f"\n❌ No working OAuth providers found.")
        print(f"💡 Run 'python oauth_setup.py' to configure providers.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
