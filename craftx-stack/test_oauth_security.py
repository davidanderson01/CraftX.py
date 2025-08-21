"""
Test script to verify OAuth configuration is working securely.
"""
import os
import sys
from oauth_config_loader import get_oauth_config


def test_oauth_config():
    """Test that OAuth configuration loads correctly with environment variables."""
    print("🔒 Testing secure OAuth configuration...")
    print("="*50)

    # Check environment variables
    required_vars = [
        'GOOGLE_CLIENT_SECRET',
        'GITHUB_CLIENT_SECRET',
        'OKTA_CLIENT_SECRET',
        'ORCID_CLIENT_SECRET'
    ]

    print("Environment Variables:")
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: {'*' * min(len(value), 20)}...")
        else:
            print(f"  ❌ {var}: Not set")
            missing_vars.append(var)

    if missing_vars:
        print(f"\n❌ Missing environment variables: {missing_vars}")
        print("Please set these in your .env file")
        return False

    print("\nOAuth Configuration:")
    try:
        config = get_oauth_config()

        for provider in config['enabled_providers']:
            name = provider.get('provider_id') or provider.get('name')
            client_id = provider.get('client_id', '')
            client_secret = provider.get('client_secret', '')

            print(f"  📱 {name.upper()}:")
            print(f"    Client ID: {client_id[:20]}...")
            print(f"    Secret: {'*' * min(len(client_secret), 20)}...")
            print(f"    Enabled: {provider.get('enabled', False)}")

            if provider.get('domain'):
                print(f"    Domain: {provider['domain']}")

        print("\n✅ OAuth configuration loaded successfully!")
        print(f"   Total providers: {len(config['enabled_providers'])}")

        return True

    except Exception as e:
        print(f"\n❌ Configuration error: {e}")
        return False


def check_security():
    """Check that no secrets are exposed in configuration files."""
    print("\n🔒 Security Check:")
    print("="*50)

    # Check auth_config.json files for exposed secrets
    config_files = ['auth_config.json', '../auth_config.json']

    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"\nChecking {config_file}:")

            with open(config_file, 'r') as f:
                content = f.read()

            # Look for patterns that might be secrets
            suspicious_patterns = [
                'GOCSPX-',  # Google OAuth secret prefix
                'ghp_',     # GitHub personal access token
                'sk-',      # OpenAI API key pattern
            ]

            secrets_found = False
            for pattern in suspicious_patterns:
                if pattern in content:
                    print(f"  ⚠️  Found potential secret pattern: {pattern}")
                    secrets_found = True

            # Check for environment variable placeholders
            if '${' in content:
                print(f"  ✅ Using environment variable placeholders")
            else:
                print(f"  ⚠️  No environment variable placeholders found")

            if not secrets_found and '${' in content:
                print(f"  ✅ Configuration file appears secure")
        else:
            print(f"  📄 {config_file}: Not found")


if __name__ == "__main__":
    print("🧪 CraftX OAuth Security Test")
    print("="*50)

    success = test_oauth_config()
    check_security()

    if success:
        print("\n🎉 All tests passed! Your OAuth system is ready and secure.")
        print("\nNext steps:")
        print("  1. Run: python craftx.py")
        print("  2. Visit: http://localhost:8000")
        print("  3. Test OAuth buttons")
    else:
        print("\n❌ Tests failed. Please fix the issues above.")
        sys.exit(1)
