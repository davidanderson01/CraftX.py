#!/usr/bin/env python3
"""
Environment checker for CraftX.py project
Helps diagnose Python and package import issues
"""

import os
import subprocess
import sys


def check_python_info():
    """Check Python interpreter information."""
    print("🐍 Python Environment Information")
    print("=" * 50)
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Python path: {sys.path[:3]}...")  # Show first 3 paths
    print()

def check_virtual_environment():
    """Check if we're in a virtual environment."""
    print("🏠 Virtual Environment Check")
    print("=" * 50)
    
    # Check for virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print("✅ Running in virtual environment")
        print(f"   Virtual env path: {sys.prefix}")
    else:
        print("❌ NOT running in virtual environment")
        print("   Consider activating your .venv:")
        print("   .venv\\Scripts\\activate")
    print()

def check_package_installations():
    """Check if required packages are installed."""
    print("📦 Package Installation Check")
    print("=" * 50)
    
    required_packages = {
        'streamlit': 'streamlit>=1.28.0',
        'pytest': 'pytest>=7.0.0',
        'requests': 'requests>=2.28.0'
    }
    
    for package, requirement in required_packages.items():
        try:
            __import__(package)
            module = sys.modules[package]
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {package}: {version}")
        except ImportError:
            print(f"❌ {package}: NOT INSTALLED")
            print(f"   Install with: pip install {requirement}")
    print()

def check_streamlit_specifically():
    """Detailed streamlit check."""
    print("🚀 Streamlit Specific Check")
    print("=" * 50)
    
    try:
        import streamlit as st
        print(f"✅ Streamlit import successful: {st.__version__}")
        
        # Check streamlit installation location
        import streamlit
        streamlit_path = streamlit.__file__
        print(f"   Streamlit location: {streamlit_path}")
        
        # Test streamlit version command
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'streamlit', 'version'], 
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print("✅ Streamlit CLI works")
                print(f"   CLI output: {result.stdout.strip()}")
            else:
                print("❌ Streamlit CLI failed")
                print(f"   Error: {result.stderr}")
        except Exception as e:
            print(f"❌ Streamlit CLI test failed: {e}")
            
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        print("   Possible solutions:")
        print("   1. Ensure you're in the correct virtual environment")
        print("   2. Install streamlit: pip install streamlit>=1.28.0")
        print("   3. Restart VS Code after installing")
    print()

def suggest_vscode_fixes():
    """Suggest VS Code specific fixes."""
    print("🔧 VS Code Configuration Suggestions")
    print("=" * 50)
    print("If VS Code shows import errors but Python works:")
    print("1. Press Ctrl+Shift+P and run 'Python: Select Interpreter'")
    print("2. Select the interpreter from your .venv:")
    print(f"   {sys.executable}")
    print("3. Reload VS Code window (Ctrl+Shift+P → 'Developer: Reload Window')")
    print("4. Check if .vscode/settings.json has correct python.pythonPath")
    print()

def main():
    """Run all environment checks."""
    print("🧪 CraftX.py Environment Diagnostic Tool")
    print("=" * 60)
    print()
    
    check_python_info()
    check_virtual_environment()
    check_package_installations()
    check_streamlit_specifically()
    suggest_vscode_fixes()
    
    print("💡 Troubleshooting Tips:")
    print("- If packages are installed but VS Code shows errors, restart VS Code")
    print("- Ensure VS Code is using the correct Python interpreter (.venv)")
    print("- Check that your virtual environment is activated")
    print("- Try: pip install --upgrade streamlit")

if __name__ == "__main__":
    main()
