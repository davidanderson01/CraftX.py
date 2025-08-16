#!/usr/bin/env python3
"""
OAuth Provider Setup Script for CraftX
Run this script to configure OAuth providers for your CraftX deployment.
"""

import json
import os
import sys
from pathlib import Path

# Add parent directory to path to import auth module
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

try:
    from craftxpy.utils.auth import universal_auth
except ImportError:
    print("❌ Could not import auth module. Make sure you're running from the correct directory.")
    sys.exit(1)


def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    CraftX OAuth Setup                        ║
    ║                  Configure OAuth Providers                   ║
    ╚══════════════════════════════════════════════════════════════╝
    """)


def get_provider_instructions(provider):
    """Get setup instructions for each provider"""
    instructions = {
        "google": """
        🔍 Google OAuth Setup:
        1. Go to Google Cloud Console (https://console.cloud.google.com/)
        2. Create a new project or select existing project
        3. Enable Google+ API
        4. Go to Credentials → Create credentials → OAuth 2.0 Client IDs
        5. Choose 'Web application'
        6. Add authorized redirect URI: http://localhost:8000/auth/callback/google
        7. Copy the Client ID and Client Secret
        """,

        "github": """
        🐙 GitHub OAuth Setup:
        1. Go to GitHub Settings → Developer settings → OAuth Apps
        2. Click 'New OAuth App'
        3. Set Authorization callback URL: http://localhost:8000/auth/callback/github
        4. Copy the Client ID and generate a Client Secret
        """,

        "microsoft": """
        🔷 Microsoft OAuth Setup:
        1. Go to Azure Portal (https://portal.azure.com/)
        2. Navigate to Azure Active Directory → App registrations
        3. Click 'New registration'
        4. Set redirect URI: http://localhost:8000/auth/callback/microsoft
        5. Copy Application (client) ID and create a client secret
        """,

        "okta": """
        🏢 Okta OAuth Setup:
        1. Go to Okta Developer Console (https://dev.okta.com/)
        2. Create a new app integration
        3. Choose 'OIDC - OpenID Connect' → 'Web Application'
        4. Set Sign-in redirect URIs: http://localhost:8000/auth/callback/okta
        5. Copy Client ID and Client Secret
        6. Note your Okta domain (e.g., dev-123456.okta.com)
        """,

        "orcid": """
        🎓 ORCID OAuth Setup:
        1. Go to ORCID Developer Tools (https://orcid.org/developer-tools)
        2. Register for a developer account
        3. Create a new application
        4. Set redirect URI: http://localhost:8000/auth/callback/orcid
        5. Copy Client ID and Client Secret
        """
    }

    return instructions.get(provider, f"No specific instructions available for {provider}")


def configure_provider():
    """Interactive provider configuration"""
    # Initialize auth system
    universal_auth.initialize_auth()

    # List available providers
    providers = list(universal_auth.supported_providers.keys())

    print("\n📋 Available OAuth Providers:")
    for i, provider in enumerate(providers, 1):
        provider_info = universal_auth.supported_providers[provider]
        print(f"  {i}. {provider_info['name']} ({provider})")

    print(f"  {len(providers) + 1}. View current configuration")
    print(f"  {len(providers) + 2}. Exit")

    try:
        choice = int(
            input(f"\nSelect a provider (1-{len(providers) + 2}): ")) - 1

        if choice == len(providers):  # View configuration
            view_configuration()
            return True
        elif choice == len(providers) + 1:  # Exit
            return False
        elif 0 <= choice < len(providers):
            provider_id = providers[choice]
            setup_provider(provider_id)
            return True
        else:
            print("❌ Invalid selection")
            return True

    except (ValueError, KeyboardInterrupt):
        print("\n👋 Goodbye!")
        return False


def setup_provider(provider_id):
    """Setup a specific OAuth provider"""
    provider_info = universal_auth.supported_providers[provider_id]

    print(f"\n🔧 Configuring {provider_info['name']} ({provider_id})")
    print(get_provider_instructions(provider_id))

    # Get credentials from user
    client_id = input(f"\nEnter {provider_info['name']} Client ID: ").strip()
    if not client_id:
        print("❌ Client ID is required")
        return

    client_secret = input(
        f"Enter {provider_info['name']} Client Secret: ").strip()
    if not client_secret:
        print("❌ Client Secret is required")
        return

    domain = ""
    if provider_info.get("requires_domain"):
        domain = input(
            f"Enter {provider_info['name']} Domain (e.g., your-domain.okta.com): ").strip()
        if not domain:
            print("❌ Domain is required for this provider")
            return

    # Save configuration
    try:
        universal_auth.add_provider_config(
            provider_id, client_id, client_secret, domain)
        print(f"✅ {provider_info['name']} configured successfully!")

        # Show test URL
        test_url = f"http://localhost:8000/auth/{provider_id}"
        print(f"🔗 Test URL: {test_url}")

    except Exception as e:
        print(f"❌ Configuration failed: {e}")


def view_configuration():
    """View current OAuth configuration"""
    try:
        config = universal_auth.get_auth_config()

        print("\n📊 Current OAuth Configuration:")
        print("=" * 50)

        if not config["enabled_providers"]:
            print("No providers configured yet.")
            return

        for provider_config in config["enabled_providers"]:
            provider_id = provider_config["provider_id"]
            provider_info = universal_auth.supported_providers.get(
                provider_id, {})

            print(f"\n🔸 {provider_info.get('name', provider_id)}")
            print(f"   Provider ID: {provider_id}")
            print(f"   Client ID: {provider_config['client_id'][:8]}...")
            print(
                f"   Has Secret: {'Yes' if provider_config.get('client_secret') else 'No'}")
            if provider_config.get('domain'):
                print(f"   Domain: {provider_config['domain']}")

            test_url = f"http://localhost:8000/auth/{provider_id}"
            print(f"   Test URL: {test_url}")

        print("\n" + "=" * 50)

    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")


def main():
    """Main setup loop"""
    print_banner()

    # Check if auth module is available
    try:
        universal_auth.initialize_auth()
        print("✅ Authentication system initialized")
    except Exception as e:
        print(f"❌ Failed to initialize auth system: {e}")
        return

    print("\n🚀 Ready to configure OAuth providers!")
    print("Make sure your CraftX server is running on http://localhost:8000")

    while True:
        if not configure_provider():
            break

    print("\n🎉 OAuth setup complete!")
    print("Start your CraftX server with: python craftx.py")
    print("Then visit: http://localhost:8000")


if __name__ == "__main__":
    main()
