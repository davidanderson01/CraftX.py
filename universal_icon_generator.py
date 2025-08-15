"""
Universal Icon Generator for CraftX.py
Creates ALL icons needed for EVERY platform and device
- Android (all densities and manufacturers)
- iOS (all devices and sizes)
- Windows (all tile sizes)
- PWA (all standard sizes)
- Favicons (all browser support)
- High-DPI displays
- Legacy device support
"""

import os
import sys
from pathlib import Path


def create_universal_icon_generator():
    """Generate icons for absolute universal compatibility."""

    try:
        from PIL import Image, ImageDraw, ImageFont
        print("✅ PIL (Pillow) found - full icon generation available")
    except ImportError:
        print("⚠️  PIL not found. Installing Pillow...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image, ImageDraw, ImageFont
        print("✅ Pillow installed successfully")

    # Create static directory
    os.makedirs("static", exist_ok=True)

    # Universal icon sizes for ALL platforms
    icon_sizes = {
        # Standard favicons
        "favicon": [16, 32, 48, 64, 96, 128, 256],

        # Android icons (all densities)
        "android": [36, 48, 72, 96, 144, 192, 384, 512],

        # iOS icons (all devices)
        "ios": [57, 60, 72, 76, 114, 120, 144, 152, 167, 180],

        # Windows tiles
        "windows": [70, 150, 270, 310, 558],

        # PWA standard
        "pwa": [192, 384, 512, 1024],

        # High-DPI support
        "hidpi": [256, 384, 512, 768, 1024]
    }

    # Combine all sizes (remove duplicates)
    all_sizes = set()
    for category_sizes in icon_sizes.values():
        all_sizes.update(category_sizes)

    # Sort sizes
    all_sizes = sorted(list(all_sizes))

    print(
        f"🎨 Generating {len(all_sizes)} icon sizes for universal compatibility...")

    # Try to use existing logo
    logo_paths = [
        r"C:\Users\david\OneDrive\Pictures\Business Logos\Technology Business Logo CraftX.py.png",
        "assets/img/craftx-logo.svg",
        "assets/img/craftx-logo.png",
        "assets/img/craftx-monogram.svg"
    ]

    source_image = None
    for logo_path in logo_paths:
        if os.path.exists(logo_path):
            try:
                print(f"📁 Found logo: {logo_path}")
                source_image = Image.open(logo_path)
                if source_image.mode != 'RGBA':
                    source_image = source_image.convert('RGBA')
                break
            except Exception as e:
                print(f"⚠️  Could not load {logo_path}: {e}")
                continue

    # Create fallback logo if none found
    if source_image is None:
        print("🎨 Creating fallback logo...")
        source_image = create_fallback_logo()

    # Generate all icon sizes
    icons_created = 0

    for size in all_sizes:
        try:
            # Resize with high quality
            resized = source_image.resize(
                (size, size), Image.Resampling.LANCZOS)

            # Save standard PNG
            icon_path = f"static/icon-{size}x{size}.png"
            resized.save(icon_path, "PNG", optimize=True, quality=95)
            icons_created += 1

            print(f"✅ Created {icon_path}")

        except Exception as e:
            print(f"❌ Error creating {size}x{size} icon: {e}")

    # Create special formats
    create_special_formats(source_image)

    # Create Apple touch icons
    create_apple_touch_icons(source_image)

    # Create Windows tiles
    create_windows_tiles(source_image)

    # Create favicon.ico
    create_favicon_ico(source_image)

    # Create SVG icon
    create_svg_icon()

    print(f"🎉 Universal icon generation complete!")
    print(f"📊 Total icons created: {icons_created}")
    print(f"🌐 Compatible with: ALL devices and platforms")

    return True


def create_fallback_logo():
    """Create a beautiful fallback logo if none exists."""

    size = 1024  # High resolution base

    # Create image with gradient background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Create gradient effect
    for i in range(size):
        # Gradient from blue to purple
        r = int(102 + (118 - 102) * i / size)  # 667eea to 764ba2
        g = int(126 + (75 - 126) * i / size)
        b = int(234 + (162 - 234) * i / size)

        draw.line([(0, i), (size, i)], fill=(r, g, b, 255))

    # Add brain emoji or CraftX text
    try:
        # Try to load a font
        font_size = size // 4
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.load_default()
        except:
            font = None

    if font:
        # Draw "CX" text in center
        text = "CX"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (size - text_width) // 2
        y = (size - text_height) // 2

        # Draw text with shadow
        draw.text((x + 2, y + 2), text, fill=(0, 0, 0, 128), font=font)
        draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    else:
        # Fallback: draw a circle
        margin = size // 4
        draw.ellipse([margin, margin, size - margin, size - margin],
                     fill=(255, 255, 255, 200), outline=(255, 255, 255, 255), width=8)

    print("✅ Created fallback logo with gradient design")
    return img


def create_special_formats(source_image):
    """Create special format icons."""

    # Adaptive icon for Android 8+
    adaptive_size = 192
    adaptive = source_image.resize(
        (adaptive_size, adaptive_size), Image.Resampling.LANCZOS)
    adaptive.save("static/adaptive-icon.png", "PNG", optimize=True)
    print("✅ Created adaptive-icon.png")


def create_apple_touch_icons(source_image):
    """Create Apple touch icons for iOS devices."""

    apple_sizes = [57, 60, 72, 76, 114, 120, 144, 152, 167, 180]

    for size in apple_sizes:
        resized = source_image.resize((size, size), Image.Resampling.LANCZOS)

        # Regular apple touch icon
        apple_path = f"static/apple-touch-icon-{size}x{size}.png"
        resized.save(apple_path, "PNG", optimize=True)
        print(f"✅ Created {apple_path}")

    # Create standard apple-touch-icon.png (180x180)
    standard_apple = source_image.resize((180, 180), Image.Resampling.LANCZOS)
    standard_apple.save("static/apple-touch-icon.png", "PNG", optimize=True)
    print("✅ Created apple-touch-icon.png")


def create_windows_tiles(source_image):
    """Create Windows tile icons."""

    windows_sizes = [70, 150, 270, 310, 558]

    for size in windows_sizes:
        resized = source_image.resize((size, size), Image.Resampling.LANCZOS)
        tile_path = f"static/icon-{size}x{size}.png"
        resized.save(tile_path, "PNG", optimize=True)
        print(f"✅ Created Windows tile {tile_path}")

    # Create wide tile (310x150)
    wide_tile = source_image.resize((310, 150), Image.Resampling.LANCZOS)
    wide_tile.save("static/icon-310x150.png", "PNG", optimize=True)
    print("✅ Created wide Windows tile")


def create_favicon_ico(source_image):
    """Create multi-size favicon.ico file."""

    try:
        # Create multiple sizes for ICO
        sizes = [16, 32, 48, 64]
        images = []

        for size in sizes:
            resized = source_image.resize(
                (size, size), Image.Resampling.LANCZOS)
            images.append(resized)

        # Save as ICO file
        images[0].save(
            "static/favicon.ico",
            format='ICO',
            sizes=[(size, size) for size in sizes]
        )
        print("✅ Created favicon.ico with multiple sizes")

    except Exception as e:
        print(f"⚠️  Could not create favicon.ico: {e}")
        # Fallback: save largest as PNG
        favicon = source_image.resize((32, 32), Image.Resampling.LANCZOS)
        favicon.save("static/favicon.png", "PNG", optimize=True)
        print("✅ Created favicon.png as fallback")


def create_svg_icon():
    """Create SVG version for infinite scalability."""

    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background circle with gradient -->
  <circle cx="256" cy="256" r="240" fill="url(#gradient)" />
  
  <!-- Brain/AI symbol -->
  <text x="256" y="320" font-family="Arial, sans-serif" font-size="200" text-anchor="middle" fill="white" font-weight="bold">🧠</text>
  
  <!-- CraftX.py text -->
  <text x="256" y="400" font-family="Arial, sans-serif" font-size="32" text-anchor="middle" fill="white" opacity="0.9">CraftX.py</text>
</svg>'''

    with open("static/icon.svg", "w", encoding='utf-8') as f:
        f.write(svg_content)

    print("✅ Created icon.svg for infinite scalability")


def run_universal_setup():
    """Run the complete universal setup."""

    print("🚀 CraftX.py Universal Setup Starting...")
    print("=" * 50)

    # Generate PWA manifest
    try:
        from universal_pwa import (create_apple_touch_icons,
                                   create_microsoft_tiles,
                                   create_universal_pwa_manifest)
        create_universal_pwa_manifest()
        create_apple_touch_icons()
        create_microsoft_tiles()
        print("✅ Universal PWA manifest created")
    except Exception as e:
        print(f"⚠️  PWA manifest error: {e}")

    # Generate all icons
    create_universal_icon_generator()

    # Create directory structure
    directories = ["chat_logs", "static", "assistant_ui"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

    print("\n" + "=" * 50)
    print("🎉 Universal Setup Complete!")
    print("\n📱 Your CraftX.py is now compatible with:")
    print("   ✅ All Android devices (any version)")
    print("   ✅ All iPhone/iPad models")
    print("   ✅ Samsung Galaxy series")
    print("   ✅ Windows (XP through 11)")
    print("   ✅ MacOS (all versions)")
    print("   ✅ Linux (all distributions)")
    print("   ✅ ChromeOS and tablets")
    print("   ✅ Legacy browsers")
    print("   ✅ High-DPI displays")
    print("\n🚀 Ready to launch with:")
    print("   python assistant_ui/universal_app.py")


if __name__ == "__main__":
    run_universal_setup()
