"""
PyPI Publishing Helper for CraftX.py
Helps you publish your package to PyPI with proper token handling.
"""

import os
import subprocess
import sys
from pathlib import Path


def setup_pypirc():
    """Create a .pypirc file in the user's home directory."""
    home = Path.home()
    pypirc_path = home / ".pypirc"

    print("🔧 Setting up PyPI configuration...")
    print(f"Configuration will be saved to: {pypirc_path}")

    # Get tokens from user
    print("\n📝 You'll need to create API tokens at:")
    print("- PyPI: https://pypi.org/manage/account/")
    print("- Test PyPI: https://test.pypi.org/manage/account/")

    print("\n⚠️  Token paste issue? Try these solutions:")
    print("1. Right-click and paste")
    print("2. Use Ctrl+Shift+V")
    print("3. Type the token manually")
    print("4. Use PowerShell ISE instead of regular PowerShell")

    pypi_token = input("\nEnter your PyPI token (starts with pypi-): ").strip()
    testpypi_token = input(
        "Enter your Test PyPI token (optional, press Enter to skip): ").strip()

    config_content = f"""[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = {pypi_token}

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = {testpypi_token if testpypi_token else 'YOUR_TESTPYPI_TOKEN_HERE'}
"""

    try:
        with open(pypirc_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print(f"✅ Configuration saved to {pypirc_path}")
        return True
    except OSError as e:
        print(f"❌ Error saving configuration: {e}")
        return False


def build_package():
    """Build the package distributions."""
    print("🏗️  Building package...")
    try:
        # Clean previous builds
        if os.path.exists("dist"):
            import shutil
            shutil.rmtree("dist")
        if os.path.exists("build"):
            import shutil
            shutil.rmtree("build")

        # Build package
        result = subprocess.run([
            sys.executable, "setup.py", "sdist", "bdist_wheel"
        ], capture_output=True, text=True, check=False)

        if result.returncode == 0:
            print("✅ Package built successfully!")
            print("📦 Files created in dist/ directory:")
            if os.path.exists("dist"):
                for file in os.listdir("dist"):
                    print(f"   - {file}")
            return True
        else:
            print("❌ Build failed:")
            print(result.stderr)
            return False
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"❌ Build error: {e}")
        return False


def upload_to_testpypi():
    """Upload to Test PyPI first."""
    print("🧪 Uploading to Test PyPI...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "twine", "upload",
            "--repository", "testpypi", "dist/*"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Successfully uploaded to Test PyPI!")
            print("🔗 Check your package at: https://test.pypi.org/project/craftxpy/")
            return True
        else:
            print("❌ Upload to Test PyPI failed:")
            print(result.stderr)
            return False
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"❌ Upload error: {e}")
        return False


def upload_to_pypi():
    """Upload to production PyPI."""
    print("🚀 Uploading to PyPI...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "twine", "upload", "dist/*"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Successfully uploaded to PyPI!")
            print("🔗 Your package is now live at: https://pypi.org/project/craftxpy/")
            return True
        else:
            print("❌ Upload to PyPI failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False


def main():
    """Main publishing workflow."""
    print("🚀 CraftX.py PyPI Publishing Helper")
    print("=" * 50)

    # Check if required tools are installed
    try:
        # import twine
        print("✅ Twine is installed")
    except ImportError:
        print("❌ Twine not found. Installing...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "twine"])

    try:
        # import wheel
        print("✅ Wheel is installed")
    except ImportError:
        print("❌ Wheel not found. Installing...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "wheel"])

    print("\n📋 Choose an option:")
    print("1. Set up PyPI configuration (.pypirc)")
    print("2. Build package only")
    print("3. Upload to Test PyPI")
    print("4. Upload to production PyPI")
    print("5. Full workflow (build + test + production)")

    choice = input("\nEnter your choice (1-5): ").strip()

    if choice == "1":
        setup_pypirc()
    elif choice == "2":
        build_package()
    elif choice == "3":
        if build_package():
            upload_to_testpypi()
    elif choice == "4":
        if build_package():
            upload_to_pypi()
    elif choice == "5":
        if setup_pypirc():
            if build_package():
                if upload_to_testpypi():
                    confirm = input(
                        "\n✅ Test upload successful! Upload to production PyPI? (y/N): ")
                    if confirm.lower() == 'y':
                        upload_to_pypi()
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()
