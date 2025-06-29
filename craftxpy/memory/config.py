"""Storage configuration for CraftX.py."""

import os
from typing import Dict, Any


class StorageConfig:
    """Configuration management for storage backends."""

    # Default configurations for different storage types
    DEFAULT_CONFIGS = {
        "development": {
            "type": "json",
            "path": "chat_logs",
            "description": "Simple JSON file storage for development"
        },

        "production_sqlite": {
            "type": "sqlite",
            "db_path": "craftx_production.db",
            "description": "SQLite database for production use"
        },

        "production_hybrid": {
            "type": "hybrid",
            "primary": {
                "type": "sqlite",
                "db_path": "craftx_primary.db"
            },
            "secondary": [
                {
                    "type": "json",
                    "path": "chat_logs_backup"
                }
            ],
            "description": "Hybrid storage with SQLite primary and JSON backup"
        },

        "cloud_ready": {
            "type": "hybrid",
            "primary": {
                "type": "sqlite",
                "db_path": "craftx.db"
            },
            "secondary": [
                {
                    "type": "json",
                    "path": "local_backup"
                }
            ],
            "cloud_storage": {
                "enabled": True,
                "provider": "azure",  # azure, aws, gcp
                "sync_interval": 300,  # seconds
                "backup_retention": 30  # days
            },
            "description": "Cloud-ready storage with local fallback"
        }
    }

    @classmethod
    def get_config(cls, profile_name: str = "development") -> Dict[str, Any]:
        """Get storage configuration for a specific profile.

        Args:
            profile_name: Configuration profile name

        Returns:
            Storage configuration dictionary
        """
        config = cls.DEFAULT_CONFIGS.get(profile_name)
        if not config:
            available = list(cls.DEFAULT_CONFIGS.keys())
            raise ValueError(
                f"Unknown profile '{profile_name}'. Available: {available}")

        # Apply environment variable overrides
        config = cls._apply_env_overrides(config.copy())

        return config

    @classmethod
    def _apply_env_overrides(cls, config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides to configuration.

        Args:
            config: Base configuration

        Returns:
            Configuration with environment overrides applied
        """
        # Database path override
        if "db_path" in config and "CRAFTX_DB_PATH" in os.environ:
            config["db_path"] = os.environ["CRAFTX_DB_PATH"]

        # JSON storage path override
        if "path" in config and "CRAFTX_STORAGE_PATH" in os.environ:
            config["path"] = os.environ["CRAFTX_STORAGE_PATH"]

        # Storage type override
        if "CRAFTX_STORAGE_TYPE" in os.environ:
            config["type"] = os.environ["CRAFTX_STORAGE_TYPE"]

        return config

    @classmethod
    def list_profiles(cls) -> Dict[str, str]:
        """List available configuration profiles.

        Returns:
            Dictionary of profile names and descriptions
        """
        return {
            name: config.get("description", "No description")
            for name, config in cls.DEFAULT_CONFIGS.items()
        }


# Storage requirements for different use cases
STORAGE_REQUIREMENTS = {
    "small_project": {
        "recommended": "development",
        "max_sessions": 100,
        "max_messages_per_session": 1000,
        "storage_estimate": "< 10 MB"
    },

    "medium_project": {
        "recommended": "production_sqlite",
        "max_sessions": 10000,
        "max_messages_per_session": 5000,
        "storage_estimate": "100 MB - 1 GB"
    },

    "large_project": {
        "recommended": "production_hybrid",
        "max_sessions": 100000,
        "max_messages_per_session": 10000,
        "storage_estimate": "1 GB - 10 GB"
    },

    "enterprise": {
        "recommended": "cloud_ready",
        "max_sessions": "unlimited",
        "max_messages_per_session": "unlimited",
        "storage_estimate": "> 10 GB",
        "additional_features": [
            "Cloud backup",
            "Disaster recovery",
            "Multi-region replication",
            "Advanced analytics"
        ]
    }
}


def recommend_storage_config(project_size: str = "small_project") -> Dict[str, Any]:
    """Recommend storage configuration based on project size.

    Args:
        project_size: Size category of the project

    Returns:
        Recommended storage configuration
    """
    if project_size not in STORAGE_REQUIREMENTS:
        available = list(STORAGE_REQUIREMENTS.keys())
        raise ValueError(
            f"Unknown project size '{project_size}'. Available: {available}")

    requirements = STORAGE_REQUIREMENTS[project_size]
    recommended_profile = requirements["recommended"]

    return {
        "profile": recommended_profile,
        "config": StorageConfig.get_config(recommended_profile),
        "requirements": requirements
    }


if __name__ == "__main__":
    # Example usage
    print("Available storage profiles:")
    for profile, description in StorageConfig.list_profiles().items():
        print(f"  {profile}: {description}")

    print("\nStorage recommendations:")
    for size in STORAGE_REQUIREMENTS:
        recommendation = recommend_storage_config(size)
        print(f"  {size}: {recommendation['profile']}")
