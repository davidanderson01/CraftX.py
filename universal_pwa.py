"""
Universal PWA Manifest Generator for CraftX.py
Compatible with ALL devices: Android, iOS, Samsung, Windows, Mac, Linux
"""

import json
import os
from pathlib import Path


def create_universal_pwa_manifest():
    """Create universal PWA manifest for maximum device compatibility."""

    manifest = {
        "name": "CraftX.py AI Assistant",
        "short_name": "CraftX.py",
        "description": "Universal AI-powered assistant framework - works on any device",
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "orientation": "any",
        "background_color": "#667eea",
        "theme_color": "#764ba2",
        "lang": "en-US",
        "dir": "ltr",

        # Universal compatibility flags
        "prefer_related_applications": False,
        "display_override": ["window-controls-overlay", "standalone", "minimal-ui", "browser"],

        # Categories for app stores
        "categories": [
            "productivity",
            "utilities",
            "developer",
            "business",
            "education"
        ],

        # Universal icon set for ALL devices and resolutions
        "icons": [
            # Android (all densities)
            {"src": "static/icon-36x36.png", "sizes": "36x36",
                "type": "image/png", "density": "0.75", "purpose": "any maskable"},
            {"src": "static/icon-48x48.png", "sizes": "48x48",
                "type": "image/png", "density": "1.0", "purpose": "any maskable"},
            {"src": "static/icon-72x72.png", "sizes": "72x72",
                "type": "image/png", "density": "1.5", "purpose": "any maskable"},
            {"src": "static/icon-96x96.png", "sizes": "96x96",
                "type": "image/png", "density": "2.0", "purpose": "any maskable"},
            {"src": "static/icon-144x144.png", "sizes": "144x144",
                "type": "image/png", "density": "3.0", "purpose": "any maskable"},
            {"src": "static/icon-192x192.png", "sizes": "192x192",
                "type": "image/png", "density": "4.0", "purpose": "any maskable"},

            # iOS specific sizes
            {"src": "static/icon-120x120.png", "sizes": "120x120",
                "type": "image/png", "purpose": "any"},
            {"src": "static/icon-152x152.png", "sizes": "152x152",
                "type": "image/png", "purpose": "any"},
            {"src": "static/icon-167x167.png", "sizes": "167x167",
                "type": "image/png", "purpose": "any"},
            {"src": "static/icon-180x180.png", "sizes": "180x180",
                "type": "image/png", "purpose": "any"},

            # Windows tiles
            {"src": "static/icon-128x128.png", "sizes": "128x128",
                "type": "image/png", "purpose": "any"},
            {"src": "static/icon-270x270.png", "sizes": "270x270",
                "type": "image/png", "purpose": "any"},
            {"src": "static/icon-558x558.png", "sizes": "558x558",
                "type": "image/png", "purpose": "any"},

            # High-res for all platforms
            {"src": "static/icon-384x384.png", "sizes": "384x384",
                "type": "image/png", "purpose": "any maskable"},
            {"src": "static/icon-512x512.png", "sizes": "512x512",
                "type": "image/png", "purpose": "any maskable"},
            {"src": "static/icon-1024x1024.png", "sizes": "1024x1024",
                "type": "image/png", "purpose": "any"},

            # Adaptive icons for Android 8+
            {"src": "static/adaptive-icon.png", "sizes": "192x192",
                "type": "image/png", "purpose": "maskable"},

            # Vector icon for infinite scaling
            {"src": "static/icon.svg", "sizes": "any",
                "type": "image/svg+xml", "purpose": "any maskable"}
        ],

        # Universal shortcuts that work on all platforms
        "shortcuts": [
            {
                "name": "New Chat",
                "short_name": "Chat",
                "description": "Start a new AI conversation",
                "url": "/?action=new_chat",
                "icons": [{"src": "static/icon-96x96.png", "sizes": "96x96", "type": "image/png"}]
            },
            {
                "name": "Code Assistant",
                "short_name": "Code",
                "description": "Get coding help",
                "url": "/?action=code_help",
                "icons": [{"src": "static/icon-96x96.png", "sizes": "96x96", "type": "image/png"}]
            },
            {
                "name": "Quick Tools",
                "short_name": "Tools",
                "description": "Access development tools",
                "url": "/?action=tools",
                "icons": [{"src": "static/icon-96x96.png", "sizes": "96x96", "type": "image/png"}]
            },
            {
                "name": "Documentation",
                "short_name": "Docs",
                "description": "View documentation",
                "url": "/?action=docs",
                "icons": [{"src": "static/icon-96x96.png", "sizes": "96x96", "type": "image/png"}]
            }
        ],

        # File handlers for universal file support
        "file_handlers": [
            {
                "action": "/?handler=code",
                "accept": {
                    "text/plain": [".py", ".js", ".ts", ".html", ".css", ".json", ".md"],
                    "text/x-python": [".py"],
                    "application/javascript": [".js"],
                    "text/html": [".html"],
                    "text/css": [".css"],
                    "application/json": [".json"]
                }
            }
        ],

        # Protocol handlers
        "protocol_handlers": [
            {
                "protocol": "web+craftx",
                "url": "/?handler=%s"
            }
        ],

        # Share target for receiving shared content
        "share_target": {
            "action": "/?share",
            "method": "POST",
            "enctype": "multipart/form-data",
            "params": {
                "title": "title",
                "text": "text",
                "url": "url",
                "files": [
                    {
                        "name": "files",
                        "accept": ["text/*", "image/*", ".py", ".js", ".ts", ".json", ".md"]
                    }
                ]
            }
        },

        # Capture links
        "capture_links": "new-client",

        # Launch handler
        "launch_handler": {
            "client_mode": ["navigate-new", "navigate-existing", "auto"]
        },

        # Edge sidebar support
        "edge_side_panel": {
            "preferred_width": 400
        },

        # Related applications (for app stores)
        "related_applications": [
            {
                "platform": "web",
                "url": "https://craftx.elevatecraft.org"
            }
        ]
    }

    # Create static directory if it doesn't exist
    os.makedirs("static", exist_ok=True)

    # Write universal manifest
    with open("static/manifest.json", "w", encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("✅ Universal PWA manifest created at static/manifest.json")
    print("🌐 Compatible with: Android, iOS, Windows, Mac, Linux, ChromeOS")
    return True


def create_apple_touch_icons():
    """Create Apple-specific touch icons for iOS compatibility."""

    apple_sizes = [
        57, 60, 72, 76, 114, 120, 144, 152, 167, 180
    ]

    # Create apple-touch-icon files
    for size in apple_sizes:
        icon_file = f"static/apple-touch-icon-{size}x{size}.png"
        # This will be created by the icon generator
        print(f"📱 Apple touch icon target: {icon_file}")

    # Standard apple-touch-icon
    print("📱 Standard apple-touch-icon: static/apple-touch-icon.png")

    return apple_sizes


def create_microsoft_tiles():
    """Create Microsoft tile configurations for Windows."""

    # browserconfig.xml for Windows tiles
    browserconfig = '''<?xml version="1.0" encoding="utf-8"?>
<browserconfig>
    <msapplication>
        <tile>
            <square70x70logo src="static/icon-70x70.png"/>
            <square150x150logo src="static/icon-150x150.png"/>
            <wide310x150logo src="static/icon-310x150.png"/>
            <square310x310logo src="static/icon-310x310.png"/>
            <TileColor>#667eea</TileColor>
        </tile>
    </msapplication>
</browserconfig>'''

    with open("static/browserconfig.xml", "w", encoding='utf-8') as f:
        f.write(browserconfig)

    print("🪟 Microsoft tile config created: static/browserconfig.xml")
    return True


def create_favicon_set():
    """Create complete favicon set for universal browser support."""

    favicon_sizes = [16, 32, 48, 64, 96, 128, 256]

    print("🌐 Favicon targets created for sizes:", favicon_sizes)
    return favicon_sizes

# Legacy function for backward compatibility


def create_pwa_manifest():
    """Legacy function - use create_universal_pwa_manifest instead."""
    return create_universal_pwa_manifest()


if __name__ == "__main__":
    print("🚀 Creating Universal PWA Manifest...")
    create_universal_pwa_manifest()
    create_apple_touch_icons()
    create_microsoft_tiles()
    create_favicon_set()
    print("✅ Universal PWA setup complete!")
