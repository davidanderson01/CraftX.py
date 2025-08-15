#!/usr/bin/env python3
"""
Code Quality Fix Script for fix_code_quality.py
===============================================

This script automatically fixes common linting issues found by flake8.
"""

import os
import subprocess


def fix_unused_imports():
    """Fix unused import issues."""
    fixes = [
        # Remove unused imports
        ("craftxpy/memory/config.py", "from typing import Any, Dict", "# from typing import Any, Dict"),
        ("craftxpy/plugins/tools/large_storage_manager.py", "from typing import Any, Dict", "from typing import Any"),
        ("craftxpy/utils/page_builder.py", "from typing import Any, Dict, Optional", "from typing import Any"),
        ("craftxpy/utils/shell.py", "from typing import Any, Dict, List, Optional, Tuple", "from typing import Any, Dict, Optional"),
        ("demo_package.py", "from craftxpy.plugins.base import BasePlugin", "# from craftxpy.plugins.base import BasePlugin"),
        ("fix_git_config.py", "import sys", "# import sys"),
        ("prevent_git_user_repo.py", "import os", "# import os  # Used by pathlib"),
        ("publish_to_pypi.py", "import twine", "# import twine"),
        ("publish_to_pypi.py", "import wheel", "# import wheel"),
        ("run.py", "import streamlit", "# import streamlit"),
        ("run_assistant.py", "import os", "# import os"),
        ("test_import.py", "from craftxpy.memory import Logger", "# from craftxpy.memory import Logger"),
        ("test_import.py", "from craftxpy.plugins.base import BasePlugin", "# from craftxpy.plugins.base import BasePlugin"),
        ("test_import.py", "from craftxpy.utils import PageBuilder, ShellExecutor", "# from craftxpy.utils import PageBuilder, ShellExecutor"),
        ("tests/test_ui.py", "import tempfile", "# import tempfile"),
        ("tests/test_website.py", "from pathlib import Path", "# from pathlib import Path"),
    ]
    
    for filepath, old_import, new_import in fixes:
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if old_import in content:
                    content = content.replace(old_import, new_import)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✅ Fixed unused import in {filepath}")
            except OSError as e:
                print(f"❌ Error fixing {filepath}: {e}")


def fix_newlines():
    """Add missing newlines at end of files."""
    files_needing_newlines = [
        "craftxpy/agents/__init__.py",
        "craftxpy/plugins/__init__.py",
        "craftxpy/utils/__init__.py",
    ]
    
    for filepath in files_needing_newlines:
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if not content.endswith('\n'):
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content + '\n')
                    print(f"✅ Added newline to {filepath}")
            except OSError as e:
                print(f"❌ Error fixing {filepath}: {e}")


def fix_bare_except():
    """Fix bare except clauses."""
    filepath = "craftxpy/utils/shell.py"
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace bare except with specific exception
            content = content.replace("except:", "except Exception:")
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Fixed bare except in {filepath}")
        except Exception as e:
            print(f"❌ Error fixing {filepath}: {e}")


def fix_whitespace_issues():
    """Fix trailing whitespace and blank line issues."""
    
    def clean_file(filepath):
        if not os.path.exists(filepath):
            return
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Remove trailing whitespace
            lines = [line.rstrip() + '\n' if line.strip() else '\n' for line in lines]
            
            # Remove trailing empty lines and ensure single newline at end
            while lines and lines[-1].strip() == '':
                lines.pop()
            
            if lines and not lines[-1].endswith('\n'):
                lines[-1] += '\n'
            elif lines:
                lines.append('\n')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print(f"✅ Cleaned whitespace in {filepath}")
            
        except Exception as e:
            print(f"❌ Error cleaning {filepath}: {e}")
    
    # Files with whitespace issues
    whitespace_files = [
        "assistant_ui/app.py",
        "craftxpy/__init__.py",
        "fix_git_config.py",
        "prevent_git_user_repo.py",
        "scripts/new_tool.py",
    ]
    
    for filepath in whitespace_files:
        clean_file(filepath)


def fix_line_length():
    """Fix lines that are too long."""
    fixes = [
        # Removed ineffective fix for fix_git_config.py line 15 (old and new were identical)
        {
            "file": "run.py", 
            "line": 78,
            "old": '        subprocess.check_call([sys.executable, "-m", "streamlit", "run", assistant_path])',
            "new": '        subprocess.check_call([\n            sys.executable, "-m", "streamlit", "run", assistant_path\n        ])'
        }
    ]
    
    for fix in fixes:
        filepath = fix["file"]
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if fix["old"] in content:
                    content = content.replace(fix["old"], fix["new"])
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✅ Fixed line length in {filepath}")
            except Exception as e:
                print(f"❌ Error fixing line length in {filepath}: {e}")


def add_blank_lines():
    """Add required blank lines before functions and classes."""
    
    def fix_blank_lines_in_file(filepath):
        if not os.path.exists(filepath):
            return
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            new_lines = []
            for i, line in enumerate(lines):
                # Add line to new_lines first
                new_lines.append(line)
                
                # Check if next line starts a function or class
                if i < len(lines) - 1:
                    next_line = lines[i + 1].strip()
                    if (next_line.startswith('def ') or next_line.startswith('class ')) and \
                       line.strip() != '' and not line.strip().startswith('#'):
                        # Add blank line before function/class if not already there
                        if not line.strip() == '':
                            new_lines.append('\n')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            
            print(f"✅ Fixed blank lines in {filepath}")
            
        except Exception as e:
            print(f"❌ Error fixing blank lines in {filepath}: {e}")
    
    files_needing_blank_lines = [
        "fix_git_config.py",
        "prevent_git_user_repo.py",
    ]
    
    for filepath in files_needing_blank_lines:
        fix_blank_lines_in_file(filepath)


def fix_f_string_placeholders():
    """Fix f-strings missing placeholders."""
    filepath = "prevent_git_user_repo.py"
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find and fix f-strings without placeholders
            content = content.replace('print(f"✅ Git repository root correctly set to: {toplevel}")', 
                                    'print("✅ Git repository root correctly set to:", toplevel)')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Fixed f-string in {filepath}")
        except Exception as e:
            print(f"❌ Error fixing f-string in {filepath}: {e}")


def run_autofix():
    """Run automatic fixes for common issues."""
    print("🔧 Starting automatic code quality fixes...\n")
    
    print("1. Fixing unused imports...")
    fix_unused_imports()
    
    print("\n2. Adding missing newlines...")
    fix_newlines()
    
    print("\n3. Fixing bare except clauses...")
    fix_bare_except()
    
    print("\n4. Cleaning whitespace issues...")
    fix_whitespace_issues()
    
    print("\n5. Fixing line length issues...")
    fix_line_length()
    
    print("\n6. Adding required blank lines...")
    add_blank_lines()
    
    print("\n7. Fixing f-string issues...")
    fix_f_string_placeholders()
    
    print("\n🎉 Automatic fixes completed!")
    print("\nRunning flake8 to check remaining issues...")
    
    # Run flake8 again to see remaining issues
    try:
        result = subprocess.run([
            "flake8", "--count", "--statistics", "--max-line-length=100", 
            "--ignore=E203,W503", "--exclude=.venv,build", "."
        ], capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            print("✅ All linting issues fixed!")
        else:
            print("📊 Remaining issues:")
            print(result.stdout[-500:])  # Show last 500 chars of output
            
    except Exception as e:
        print(f"❌ Error running flake8: {e}")

    run_autofix()
if __name__ == "__main__":
    run_autofix()
