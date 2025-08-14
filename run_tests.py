"""
Simple test runner for CraftX.py
Run this script to execute all tests with nice output.
"""

import os
import subprocess
import sys


def run_tests():
    """Run the test suite with detailed output."""
    print("🧪 CraftX.py Test Suite")
    print("=" * 50)

    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short",
            "--color=yes"
        ], capture_output=False, cwd=os.path.dirname(__file__), check=False)

        if result.returncode == 0:
            print("\n✅ All tests passed! The project is properly configured.")
            print("\n📊 Test Summary:")
            print("   - Project structure: ✅")
            print("   - Configuration files: ✅")
            print("   - Assistant UI: ✅")
            print("   - Dependencies: ✅")
            print("   - File handling: ✅")
        else:
            print("\n❌ Some tests failed. Check the output above for details.")

        return result.returncode == 0

    except FileNotFoundError:
        print("❌ pytest not found. Installing...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "pytest>=7.0.0"])
            print("✅ pytest installed. Please run the tests again.")
            return False
        except subprocess.CalledProcessError:
            print("❌ Failed to install pytest. Please install manually with:")
            print("   pip install pytest>=7.0.0")
            return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
