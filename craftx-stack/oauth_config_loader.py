"""
Configuration loader that safely handles OAuth secrets from environment variables.
"""
import json
import os
import re
from pathlib import Path
from typing import Dict, Any


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
        return True
    return False


def load_oauth_config(config_path: str = "auth_config.json") -> Dict[str, Any]:
    """
    Load OAuth configuration with environment variable substitution.

    Args:
        config_path: Path to the auth configuration JSON file

    Returns:
        Dictionary with OAuth configuration and secrets loaded from environment
    """
    # Load .env file first
    if load_dotenv():
        print("✅ .env file loaded for OAuth configuration")
    else:
        print("⚠️  .env file not found - using system environment variables")

    # Read the configuration template
    with open(config_path, 'r', encoding='utf-8') as f:
        config_text = f.read()

    # Substitute environment variables
    config_text = substitute_env_vars(config_text)

    # Parse as JSON
    config = json.loads(config_text)

    # Validate that all secrets were found
    validate_secrets(config)

    return config


def substitute_env_vars(text: str) -> str:
    """
    Replace ${VAR_NAME} placeholders with environment variable values.

    Args:
        text: Text containing ${VAR_NAME} placeholders

    Returns:
        Text with environment variables substituted
    """
    def replace_var(match):
        var_name = match.group(1)
        value = os.getenv(var_name)
        if value is None:
            raise ValueError(f"Environment variable {var_name} is not set")
        return value

    # Replace ${VAR_NAME} with environment variable values
    return re.sub(r'\$\{([^}]+)\}', replace_var, text)


def validate_secrets(config: Dict[str, Any]) -> None:
    """
    Validate that all OAuth secrets have been properly loaded.

    Args:
        config: OAuth configuration dictionary

    Raises:
        ValueError: If any secrets are missing or contain placeholder values
    """
    for provider in config.get('enabled_providers', []):
        client_secret = provider.get('client_secret', '')

        # Check for common placeholder patterns
        if not client_secret or client_secret.startswith('${') or client_secret in ['your_secret', 'demo_secret']:
            provider_name = provider.get('provider_id') or provider.get('name')
            raise ValueError(
                f"OAuth secret for {provider_name} is missing or invalid")


def get_oauth_config() -> Dict[str, Any]:
    """
    Convenience function to load OAuth configuration from the standard location.

    Returns:
        OAuth configuration with secrets loaded from environment variables
    """
    return load_oauth_config()


if __name__ == "__main__":
    # Test the configuration loader
    try:
        config = get_oauth_config()
        print("✅ OAuth configuration loaded successfully!")

        for provider in config['enabled_providers']:
            name = provider.get('provider_id') or provider.get('name')
            print(
                f"  📱 {name}: {'✅ configured' if provider['client_secret'] else '❌ missing secret'}")

    except Exception as e:
        print(f"❌ Configuration error: {e}")
