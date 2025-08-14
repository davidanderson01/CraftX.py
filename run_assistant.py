#!/usr/bin/env python3
"""
Simple script to run the CraftX.py assistant directly.
This bypasses the interactive menu.
"""

import os
import subprocess
import sys


def run_assistant():
    """Run the Streamlit assistant."""
    print("🚀 Starting CraftX.py Assistant...")
    try:
        # Check if streamlit is installed
        try:
            import streamlit
            print(f"Found Streamlit version: {streamlit.__version__}")
        except ImportError:
            print("Streamlit not found. Installing...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "streamlit>=1.28.0"])
            print("Streamlit installed successfully.")

        # Run the app
        print("Launching assistant...")
        subprocess.call([sys.executable, "-m", "streamlit",
                        "run", "assistant_ui/app.py"])
    except Exception as e:
        print(f"❌ Error starting assistant: {str(e)}")
        print("Attempting direct run of the Python file...")
        try:
            subprocess.call([sys.executable, "assistant_ui/app.py"])
        except Exception as e2:
            print(f"❌ Direct run also failed: {str(e2)}")


if __name__ == "__main__":
    run_assistant()
