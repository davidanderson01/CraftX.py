"""PWA Manifest Generator for CraftX.py"""

import json
import os


def create_pwa_manifest():
    """Create PWA manifest for mobile app-like experience."""

    manifest = {
        "name": "CraftX.py Assistant",
        "short_name": "CraftX.py",
        "description": "AI-powered assistant framework - anytime, anywhere",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#667eea",
        "theme_color": "#764ba2",
        "orientation": "portrait-primary",
        "scope": "/",
        "lang": "en-US",
        "categories": ["productivity", "utilities", "developer"],
        "icons": [
            {
                "src": "static/icon-72x72.png",
                "sizes": "72x72",
                "type": "image/png",
                "purpose": "maskable any"
            },
            {
                "src": "static/icon-96x96.png",
                "sizes": "96x96",
                "type": "image/png",
                "purpose": "maskable any"
            },
            {
                "src": "static/icon-128x128.png",
                "sizes": "128x128",
                "type": "image/png",
                "purpose": "maskable any"
            },
            {
                "src": "static/icon-144x144.png",
                "sizes": "144x144",
                "type": "image/png",
                "purpose": "maskable any"
            },
            {
                "src": "static/icon-152x152.png",
                "sizes": "152x152",
                "type": "image/png",
                "purpose": "maskable any"
            },
            {
                "src": "static/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "maskable any"
            },
            {
                "src": "static/icon-384x384.png",
                "sizes": "384x384",
                "type": "image/png",
                "purpose": "maskable any"
            },
            {
                "src": "static/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "maskable any"
            }
        ],
        "shortcuts": [
            {
                "name": "New Chat",
                "short_name": "Chat",
                "description": "Start a new conversation",
                "url": "/?action=new_chat",
                "icons": [{"src": "static/icon-96x96.png", "sizes": "96x96"}]
            },
            {
                "name": "Quick Tools",
                "short_name": "Tools",
                "description": "Access development tools",
                "url": "/?action=tools",
                "icons": [{"src": "static/icon-96x96.png", "sizes": "96x96"}]
            }
        ],
        "prefer_related_applications": False
    }

    # Create static directory if it doesn't exist
    os.makedirs("static", exist_ok=True)

    # Write manifest
    with open("static/manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print("✅ PWA manifest created at static/manifest.json")


if __name__ == "__main__":
    create_pwa_manifest()
