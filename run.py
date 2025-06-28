#!/usr/bin/env python3
"""CraftX.py Quick Start Script"""

import sys
import os
import subprocess


def check_requirements():
    """Check if required packages are installed."""
    try:
        import streamlit  # pylint: disable=import-outside-toplevel,unused-import
        return True
    except ImportError:
        return False


def install_requirements():
    """Install required packages."""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError:
        return False


def run_demo():
    """Run the demo script."""
    print("🧪 Running CraftX.py demo...")
    try:
        subprocess.call([sys.executable, "examples/demo.py"])
    except FileNotFoundError:
        print("❌ Demo file not found. Make sure you're in the CraftX.py directory.")


def run_assistant():
    """Run the Streamlit assistant."""
    print("🚀 Starting CraftX.py Assistant...")
    try:
        subprocess.call([sys.executable, "-m", "streamlit",
                        "run", "assistant_ui/app.py"])
    except FileNotFoundError:
        print("❌ Assistant app not found. Make sure you're in the CraftX.py directory.")


def run_tests():
    """Run the test suite."""
    print("🧪 Running tests...")
    try:
        subprocess.call([sys.executable, "tests/test_router.py"])
    except FileNotFoundError:
        print("❌ Test file not found. Make sure you're in the CraftX.py directory.")


def main():
    """Main menu."""
    print("🧠 CraftX.py - Python-native intelligence, modular by design")
    print("=" * 60)

    if not check_requirements():
        print("⚠️  Missing requirements. Installing...")
        if not install_requirements():
            print(
                "❌ Failed to install requirements. Please run 'pip install -r requirements.txt' manually.")
            return

    while True:
        print("\nChoose an option:")
        print("1. 🚀 Run Assistant (Streamlit UI)")
        print("2. 🧪 Run Demo")
        print("3. 🔍 Run Tests")
        print("4. 📚 View README")
        print("5. 🛠️ Create New Tool")
        print("6. ❌ Exit")

        choice = input("\nEnter choice (1-6): ").strip()

        if choice == "1":
            run_assistant()
        elif choice == "2":
            run_demo()
        elif choice == "3":
            run_tests()
        elif choice == "4":
            if os.path.exists("README.md"):
                with open("README.md", "r", encoding="utf-8") as f:
                    print("\n" + f.read()[:2000] + "...")
            else:
                print("❌ README.md not found")
        elif choice == "5":
            print("🛠️ Creating new tool...")
            subprocess.call([sys.executable, "scripts/new_tool.py"])
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()
