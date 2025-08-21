"""
Simple script to load .env file and test OAuth configuration.
"""
import os
from pathlib import Path


def load_dotenv():
    """Load environment variables from .env file"""
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print("✅ .env file loaded")
    else:
        print("❌ .env file not found")


if __name__ == "__main__":
    print("🔧 Loading environment variables...")
    load_dotenv()

    # Test OAuth secrets
    secrets = [
        'GOOGLE_CLIENT_SECRET',
        'GITHUB_CLIENT_SECRET',
        'OKTA_CLIENT_SECRET',
        'ORCID_CLIENT_SECRET'
    ]

    print("\n🔐 OAuth Secrets Status:")
    for secret in secrets:
        value = os.getenv(secret)
        if value:
            print(f"  ✅ {secret}: {value[:10]}...")
        else:
            print(f"  ❌ {secret}: Not found")

    print("\n🧪 Testing config loader...")
    try:
        from oauth_config_loader import get_oauth_config
        config = get_oauth_config()
        print("✅ OAuth configuration loaded successfully!")
        print(f"   Providers: {len(config['enabled_providers'])}")
    except Exception as e:
        print(f"❌ Config loader error: {e}")
