#!/usr/bin/env python3
"""
Deploy CraftX.py Legal Documents to Website
============================================

This script prepares the legal documents for deployment to the official website.
It ensures all documents are accessible via the FastAPI server.
"""

import os
import shutil
import sys
from pathlib import Path


def main():
    print("🚀 CraftX.py Legal Documents Deployment")
    print("=" * 50)

    # Get the base directory (CraftX.py root)
    base_dir = Path(__file__).parent
    craftx_stack_dir = base_dir / "craftx-stack"

    # Legal documents to deploy
    legal_docs = [
        "privacy.html",
        "terms.html",
        "eula.html",
        "nda.html"
    ]

    print(f"📁 Base directory: {base_dir}")
    print(f"📁 CraftX-Stack directory: {craftx_stack_dir}")
    print()

    # Check if all legal documents exist
    missing_docs = []
    for doc in legal_docs:
        doc_path = base_dir / doc
        if not doc_path.exists():
            missing_docs.append(doc)

    if missing_docs:
        print(f"❌ Missing legal documents: {missing_docs}")
        return False

    print("✅ All legal documents found:")
    for doc in legal_docs:
        doc_path = base_dir / doc
        size = doc_path.stat().st_size
        print(f"   📄 {doc} ({size:,} bytes)")

    print()

    # Copy documents to craftx-stack for local serving
    print("📋 Copying documents for local development...")
    for doc in legal_docs:
        src = base_dir / doc
        dst = craftx_stack_dir / doc
        try:
            shutil.copy2(src, dst)
            print(f"   ✅ {doc} → craftx-stack/")
        except Exception as e:
            print(f"   ❌ Failed to copy {doc}: {e}")
            return False

    print()

    # Update the FastAPI server to serve from local directory
    server_file = craftx_stack_dir / "craftx.py"
    if server_file.exists():
        print("🔧 Updating FastAPI server routes...")

        # Read the current server file
        with open(server_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update the file paths to use local directory instead of ../
        content = content.replace('with open("../', 'with open("./')

        # Write back the updated content
        with open(server_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print("   ✅ Updated file paths in craftx.py")

    print()

    # Create a simple test script
    test_script = craftx_stack_dir / "test_legal_docs.py"
    with open(test_script, 'w', encoding='utf-8') as f:
        f.write('''#!/usr/bin/env python3
"""Test script for legal documents accessibility"""

import os
import requests
import time
import subprocess
import sys
from pathlib import Path

def test_local_files():
    """Test if legal documents exist locally"""
    print("🧪 Testing local file accessibility...")
    
    docs = ["privacy.html", "terms.html", "eula.html", "nda.html"]
    for doc in docs:
        if os.path.exists(doc):
            size = os.path.getsize(doc)
            print(f"   ✅ {doc} ({size:,} bytes)")
        else:
            print(f"   ❌ {doc} not found")
            return False
    return True

def test_server_endpoints():
    """Test if server endpoints work"""
    print("🌐 Testing server endpoints...")
    
    base_url = "http://localhost:8000"
    endpoints = [
        "/privacy.html",
        "/terms.html", 
        "/eula.html",
        "/nda.html"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {endpoint} (HTTP {response.status_code})")
            else:
                print(f"   ❌ {endpoint} (HTTP {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {endpoint} (Connection error)")
    
    return True

if __name__ == "__main__":
    print("🔍 CraftX.py Legal Documents Test")
    print("=" * 40)
    
    if test_local_files():
        print("\\n📡 Server endpoint tests require the server to be running:")
        print("   python craftx.py")
        print("\\n🧪 Then run server tests:")
        print("   python test_legal_docs.py server")
        
        if len(sys.argv) > 1 and sys.argv[1] == "server":
            test_server_endpoints()
''')

    print(f"📝 Created test script: {test_script}")

    print()
    print("🎉 Deployment completed successfully!")
    print()
    print("📋 Next steps:")
    print("1. Start the FastAPI server:")
    print(f"   cd {craftx_stack_dir}")
    print("   python craftx.py")
    print()
    print("2. Test the legal documents:")
    print("   python test_legal_docs.py")
    print()
    print("3. Access documents at:")
    print("   http://localhost:8000/privacy.html")
    print("   http://localhost:8000/terms.html")
    print("   http://localhost:8000/eula.html")
    print("   http://localhost:8000/nda.html")
    print()
    print("4. Deploy to production:")
    print("   Push changes to GitHub (craftx.elevatecraft.org)")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
