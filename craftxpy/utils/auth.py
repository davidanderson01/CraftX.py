"""
CraftX.py Universal OAuth Authentication System
Supports: Google, Microsoft, Apple, GitHub, ORCID, OKTA, Auth0, Discord, and more
"""

import base64
import hashlib
import json
import os
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import requests
import streamlit as st


class UniversalAuth:
    """Universal OAuth authentication manager."""

    def __init__(self):
        self.auth_config_path = "auth_config.json"
        self.sessions_path = "user_sessions.json"
        self.supported_providers = {
            "google": {
                "name": "Google",
                "icon": "🔍",
                "color": "#4285F4",
                "auth_url": "https://accounts.google.com/oauth/authorize",
                "token_url": "https://oauth2.googleapis.com/token",
                "scope": "openid email profile",
                "client_id_required": True
            },
            "microsoft": {
                "name": "Microsoft",
                "icon": "🔷",
                "color": "#0078D4",
                "auth_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
                "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
                "scope": "openid email profile",
                "client_id_required": True
            },
            "apple": {
                "name": "Apple ID",
                "icon": "🍎",
                "color": "#000000",
                "auth_url": "https://appleid.apple.com/auth/authorize",
                "token_url": "https://appleid.apple.com/auth/token",
                "scope": "openid email name",
                "client_id_required": True
            },
            "github": {
                "name": "GitHub",
                "icon": "🐙",
                "color": "#181717",
                "auth_url": "https://github.com/login/oauth/authorize",
                "token_url": "https://github.com/login/oauth/access_token",
                "scope": "user:email",
                "client_id_required": True
            },
            "orcid": {
                "name": "ORCID",
                "icon": "🎓",
                "color": "#A6CE39",
                "auth_url": "https://orcid.org/oauth/authorize",
                "token_url": "https://orcid.org/oauth/token",
                "scope": "/authenticate",
                "client_id_required": True
            },
            "okta": {
                "name": "Okta",
                "icon": "🏢",
                "color": "#007DC1",
                "auth_url": "https://{domain}/oauth2/v1/authorize",
                "token_url": "https://{domain}/oauth2/v1/token",
                "scope": "openid email profile",
                "client_id_required": True,
                "requires_domain": True
            },
            "auth0": {
                "name": "Auth0",
                "icon": "🔐",
                "color": "#EB5424",
                "auth_url": "https://{domain}/authorize",
                "token_url": "https://{domain}/oauth/token",
                "scope": "openid email profile",
                "client_id_required": True,
                "requires_domain": True
            },
            "discord": {
                "name": "Discord",
                "icon": "🎮",
                "color": "#5865F2",
                "auth_url": "https://discord.com/api/oauth2/authorize",
                "token_url": "https://discord.com/api/oauth2/token",
                "scope": "identify email",
                "client_id_required": True
            },
            "linkedin": {
                "name": "LinkedIn",
                "icon": "💼",
                "color": "#0A66C2",
                "auth_url": "https://www.linkedin.com/oauth/v2/authorization",
                "token_url": "https://www.linkedin.com/oauth/v2/accessToken",
                "scope": "r_liteprofile r_emailaddress",
                "client_id_required": True
            },
            "twitter": {
                "name": "Twitter/X",
                "icon": "🐦",
                "color": "#1DA1F2",
                "auth_url": "https://twitter.com/i/oauth2/authorize",
                "token_url": "https://api.twitter.com/2/oauth2/token",
                "scope": "tweet.read users.read",
                "client_id_required": True
            }
        }
        self.initialize_auth()

    def initialize_auth(self):
        """Initialize authentication system."""
        if not os.path.exists(self.auth_config_path):
            default_config = {
                "enabled_providers": [],
                "security_settings": {
                    "session_timeout": 86400,  # 24 hours
                    "require_2fa": False,
                    "password_min_length": 8,
                    "session_encryption": True
                },
                "privacy_settings": {
                    "store_email": True,
                    "store_profile": True,
                    "analytics_enabled": False,
                    "data_retention_days": 365
                }
            }
            with open(self.auth_config_path, 'w') as f:
                json.dump(default_config, f, indent=2)

        if not os.path.exists(self.sessions_path):
            with open(self.sessions_path, 'w') as f:
                json.dump({}, f)

        # Create auth directories
        os.makedirs("auth/sessions", exist_ok=True)
        os.makedirs("auth/tokens", exist_ok=True)
        os.makedirs("auth/logs", exist_ok=True)

    def get_auth_config(self) -> Dict:
        """Get authentication configuration."""
        try:
            with open(self.auth_config_path, 'r') as f:
                return json.load(f)
        except:
            self.initialize_auth()
            return self.get_auth_config()

    def save_auth_config(self, config: Dict):
        """Save authentication configuration."""
        with open(self.auth_config_path, 'w') as f:
            json.dump(config, f, indent=2)

    def generate_oauth_url(self, provider_id: str, redirect_uri: str, state: str = None) -> str:
        """Generate OAuth authorization URL."""
        provider = self.supported_providers.get(provider_id)
        if not provider:
            raise ValueError(f"Unsupported provider: {provider_id}")

        if state is None:
            state = secrets.token_urlsafe(32)

        config = self.get_auth_config()
        provider_config = next(
            (p for p in config["enabled_providers"] if p["provider_id"] == provider_id), None)

        if not provider_config or not provider_config.get("client_id"):
            raise ValueError(
                f"Provider {provider_id} not configured or missing client_id")

        auth_params = {
            "client_id": provider_config["client_id"],
            "redirect_uri": redirect_uri,
            "scope": provider["scope"],
            "response_type": "code",
            "state": state
        }

        # Handle domain-specific providers
        auth_url = provider["auth_url"]
        if provider.get("requires_domain") and provider_config.get("domain"):
            auth_url = auth_url.format(domain=provider_config["domain"])

        # Build URL
        params_str = "&".join([f"{k}={v}" for k, v in auth_params.items()])
        return f"{auth_url}?{params_str}"

    def add_provider_config(self, provider_id: str, client_id: str, client_secret: str, domain: str = ""):
        """Add OAuth provider configuration."""
        config = self.get_auth_config()

        provider_config = {
            "provider_id": provider_id,
            "client_id": client_id,
            "client_secret": client_secret,
            "domain": domain,
            "enabled": True,
            "added_date": datetime.now().isoformat()
        }

        # Remove existing config for this provider
        config["enabled_providers"] = [
            p for p in config["enabled_providers"]
            if p["provider_id"] != provider_id
        ]

        config["enabled_providers"].append(provider_config)
        self.save_auth_config(config)
        return True

    def create_session(self, user_data: Dict, provider_id: str) -> str:
        """Create user session."""
        session_id = secrets.token_urlsafe(32)
        session_data = {
            "session_id": session_id,
            "user_data": user_data,
            "provider_id": provider_id,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=1)).isoformat(),
            "last_activity": datetime.now().isoformat()
        }

        # Load existing sessions
        try:
            with open(self.sessions_path, 'r') as f:
                sessions = json.load(f)
        except:
            sessions = {}

        sessions[session_id] = session_data

        with open(self.sessions_path, 'w') as f:
            json.dump(sessions, f, indent=2)

        return session_id

    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data."""
        try:
            with open(self.sessions_path, 'r') as f:
                sessions = json.load(f)

            session = sessions.get(session_id)
            if not session:
                return None

            # Check if session is expired
            expires_at = datetime.fromisoformat(session["expires_at"])
            if datetime.now() > expires_at:
                self.delete_session(session_id)
                return None

            # Update last activity
            session["last_activity"] = datetime.now().isoformat()
            sessions[session_id] = session

            with open(self.sessions_path, 'w') as f:
                json.dump(sessions, f, indent=2)

            return session
        except:
            return None

    def delete_session(self, session_id: str):
        """Delete session."""
        try:
            with open(self.sessions_path, 'r') as f:
                sessions = json.load(f)

            if session_id in sessions:
                del sessions[session_id]

                with open(self.sessions_path, 'w') as f:
                    json.dump(sessions, f, indent=2)

            return True
        except:
            return False

    def get_provider_info(self, provider_id: str) -> Dict:
        """Get provider information."""
        return self.supported_providers.get(provider_id, {})

    def get_all_providers(self) -> Dict:
        """Get all supported providers."""
        return self.supported_providers

    def is_provider_configured(self, provider_id: str) -> bool:
        """Check if provider is configured."""
        config = self.get_auth_config()
        return any(p["provider_id"] == provider_id for p in config["enabled_providers"])


# Global auth manager instance
universal_auth = UniversalAuth()
