#!/usr/bin/env python3
"""
Test script to validate CraftX.py Assistant app configuration
"""

import sys
import os

def test_imports():
    """Test that all required imports work."""
    try:
        import streamlit as st
        print("✅ Streamlit import successful")
        
        import json
        print("✅ JSON import successful")
        
        import datetime
        print("✅ Datetime import successful")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_structure():
    """Test that the app file structure is correct."""
    app_path = os.path.join(os.path.dirname(__file__), 'assistant_ui', 'app.py')
    
    if not os.path.exists(app_path):
        print(f"❌ App file not found: {app_path}")
        return False
    
    print(f"✅ App file found: {app_path}")
    
    # Check for key functions
    with open(app_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    required_functions = ['load_chat_history', 'save_chat_history', 'main']
    for func in required_functions:
        if f"def {func}" in content:
            print(f"✅ Function '{func}' found")
        else:
            print(f"❌ Function '{func}' missing")
            return False
    
    return True

def test_chat_logs_directory():
    """Test that chat logs directory can be created."""
    chat_logs_dir = os.path.join(os.path.dirname(__file__), 'chat_logs')
    
    try:
        os.makedirs(chat_logs_dir, exist_ok=True)
        print(f"✅ Chat logs directory ready: {chat_logs_dir}")
        return True
    except Exception as e:
        print(f"❌ Error creating chat logs directory: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing CraftX.py Assistant Configuration")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("App Structure Tests", test_app_structure),
        ("Chat Logs Directory", test_chat_logs_directory)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        if not test_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Your CraftX.py Assistant is ready to run.")
        print("\nTo start the app, run:")
        print("  streamlit run assistant_ui/app.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
