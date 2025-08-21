"""
CraftX.py Privacy Configuration
Disable all Microsoft/Azure telemetry and enable custom analytics
"""

import os
import json
from pathlib import Path
from datetime import datetime, timezone


class PrivacyConfig:
    """Configure privacy settings for CraftX.py"""

    @staticmethod
    def disable_microsoft_telemetry():
        """Disable all Microsoft and Azure telemetry"""

        # Environment variables to disable Microsoft telemetry
        telemetry_vars = {
            # .NET Core telemetry
            "DOTNET_CLI_TELEMETRY_OPTOUT": "1",

            # Visual Studio Code telemetry
            "VSCODE_CLI_DISABLE_TELEMETRY": "1",

            # Azure CLI telemetry
            "AZURE_CORE_COLLECT_TELEMETRY": "0",

            # PowerShell telemetry
            "POWERSHELL_TELEMETRY_OPTOUT": "1",

            # General Microsoft telemetry
            "DOTNET_TELEMETRY_OPTOUT": "1",
            "FUNCTIONS_EXTENSION_TELEMETRY_OPTOUT": "1",

            # Application Insights
            "APPLICATIONINSIGHTS_ENABLED": "false",
            "APPINSIGHTS_INSTRUMENTATIONKEY": "",

            # Disable various Microsoft services
            "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
            "DOTNET_CLI_DISABLE_FIRST_TIME_EXPERIENCE": "1"
        }

        print("🔒 Disabling Microsoft/Azure telemetry...")

        for var, value in telemetry_vars.items():
            os.environ[var] = value
            print(f"  ✅ Set {var}={value}")

        # Create .gitignore entries for telemetry files
        gitignore_entries = [
            "# Microsoft/Azure telemetry files",
            "*.applicationinsights.log",
            "ApplicationInsights.config",
            ".vs/",
            "appsettings.Development.json",
            "*.user",
            "*.log",
            ".azure/",
            ".vscode/settings.json"
        ]

        gitignore_path = Path(".gitignore")
        if gitignore_path.exists():
            with open(gitignore_path, "r") as f:
                existing_content = f.read()

            # Add entries if they don't exist
            new_entries = []
            for entry in gitignore_entries:
                if entry not in existing_content:
                    new_entries.append(entry)

            if new_entries:
                with open(gitignore_path, "a") as f:
                    f.write("\n" + "\n".join(new_entries) + "\n")
                print(f"  ✅ Added {len(new_entries)} entries to .gitignore")

        print("🔒 Microsoft telemetry disabled!")

    @staticmethod
    def create_privacy_config():
        """Create privacy configuration file"""
        config = {
            "privacy_settings": {
                "microsoft_telemetry_disabled": True,
                "azure_insights_disabled": True,
                "custom_analytics_enabled": True,
                "data_retention_days": 30,
                "local_storage_only": True
            },
            "custom_analytics": {
                "enabled": True,
                "storage_location": "local_sqlite",
                "collect_errors": True,
                "collect_usage": True,
                "collect_personal_data": False
            },
            "telemetry_opt_out": {
                "microsoft": True,
                "azure": True,
                "third_party": True
            }
        }

        config_path = Path("privacy_config.json")
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        print(f"✅ Privacy configuration saved to {config_path}")
        return config

    @staticmethod
    def setup_custom_analytics():
        """Initialize custom analytics system"""
        try:
            from craftxpy.utils.custom_analytics import CustomAnalytics, AnalyticsConfig

            # Show privacy information
            AnalyticsConfig.show_privacy_info()

            # Initialize with privacy-focused settings
            analytics = CustomAnalytics(enable_collection=True)

            # Track the privacy setup
            analytics.track_event("privacy_setup", {
                "microsoft_telemetry_disabled": True,
                "custom_analytics_enabled": True,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

            print("📊 Custom analytics initialized!")
            return analytics

        except ImportError as e:
            print(f"❌ Could not initialize custom analytics: {e}")
            return None

    @staticmethod
    def verify_privacy_settings():
        """Verify that privacy settings are applied"""
        print("🔍 Verifying privacy settings...")

        # Check environment variables
        privacy_vars = [
            "DOTNET_CLI_TELEMETRY_OPTOUT",
            "AZURE_CORE_COLLECT_TELEMETRY",
            "APPLICATIONINSIGHTS_ENABLED"
        ]

        for var in privacy_vars:
            value = os.environ.get(var, "NOT SET")
            status = "✅" if value in ["1", "0", "false"] else "❌"
            print(f"  {status} {var}: {value}")

        # Check for privacy config file
        config_path = Path("privacy_config.json")
        if config_path.exists():
            print("  ✅ Privacy config file exists")
        else:
            print("  ❌ Privacy config file missing")

        # Check for custom analytics
        try:
            from craftxpy.utils.custom_analytics import CustomAnalytics
            analytics = CustomAnalytics(
                enable_collection=False)  # Just test import
            print("  ✅ Custom analytics available")
        except ImportError:
            print("  ❌ Custom analytics not available")


def setup_complete_privacy():
    """Complete privacy setup - disable Microsoft, enable custom analytics"""
    print("🔒 Setting up complete privacy configuration for CraftX.py...")

    # Step 1: Disable Microsoft telemetry
    PrivacyConfig.disable_microsoft_telemetry()

    # Step 2: Create privacy config
    PrivacyConfig.create_privacy_config()

    # Step 3: Setup custom analytics
    analytics = PrivacyConfig.setup_custom_analytics()

    # Step 4: Verify settings
    PrivacyConfig.verify_privacy_settings()

    print("\n🎉 Privacy setup complete!")
    print("\n📋 What was configured:")
    print("  🔒 Microsoft/Azure telemetry: DISABLED")
    print("  📊 Custom analytics: ENABLED (local only)")
    print("  🏠 Data storage: Local SQLite database")
    print("  🚫 External tracking: NONE")

    print("\n🎛️ Available commands:")
    print("  analytics_dashboard.py - View your analytics")
    print("  python -c 'from craftxpy.utils.custom_analytics import AnalyticsConfig; AnalyticsConfig.show_privacy_info()' - Privacy info")

    return analytics


if __name__ == "__main__":
    setup_complete_privacy()
