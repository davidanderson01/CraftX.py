#!/usr/bin/env python3
"""
Git User Directory Repository Prevention Script
==============================================

This script prevents the dangerous situation where a Git repository
exists in the user's home directory, which can cause Git to track
system files and personal data.

Created: 2025-07-14
Purpose: Prevent Git from treating C:/Users/david as a repository
"""

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path


def check_and_fix_user_git_repo():
    """Check for and fix dangerous Git repository in user directory."""
    
    user_home = Path.home()
    git_dir = user_home / ".git"
    
    print(f"🔍 Checking for dangerous Git repository in: {user_home}")
    
    if git_dir.exists():
        print("⚠️  WARNING: Found .git directory in user home!")
        print("   This can cause Git to track your entire user profile!")
        
        # Create backup name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_name = f".git.DANGEROUS_BACKUP.{timestamp}"
        backup_path = user_home / backup_name
        
        try:
            print(f"📦 Moving {git_dir} to {backup_path}")
            shutil.move(str(git_dir), str(backup_path))
            print("✅ Successfully moved dangerous .git directory!")
            
            # Also create a warning file
            warning_file = user_home / "GIT_REPOSITORY_WARNING.txt"
            with open(warning_file, 'w') as f:
                f.write(f"""
WARNING: Git Repository Removed from User Directory
==================================================

Date: {datetime.now().isoformat()}
Moved from: {git_dir}
Moved to: {backup_path}

IMPORTANT: A Git repository was found in your user home directory.
This is dangerous because it can cause Git to track:
- System files (ntuser.dat, etc.)
- Personal documents
- Application data
- Sensitive configuration files

The repository has been moved to a backup location.
If you need to restore it, please move it to a proper project directory.

DO NOT restore it to your user home directory!
""")
            print(f"📝 Created warning file: {warning_file}")
            
        except Exception as e:
            print(f"❌ Error moving .git directory: {e}")
            return False
    else:
        print("✅ No dangerous .git directory found in user home")
    
    return True

def fix_git_safe_directories():
    """Fix Git safe.directory configuration."""
    
    print("\n🔧 Fixing Git safe.directory configuration...")
    
    try:
        # Remove all safe.directory entries
        subprocess.run([
            "git", "config", "--global", "--unset-all", "safe.directory"
        ], capture_output=True, text=True)
        
        # Add back only the specific project directory
        project_dir = Path(__file__).parent.resolve()
        subprocess.run([
            "git", "config", "--global", "--add", "safe.directory", str(project_dir)
        ], capture_output=True, text=True, check=True)
        
        print(f"✅ Set safe.directory to: {project_dir}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error configuring safe.directory: {e}")
        return False
    
    return True

def verify_git_status():
    """Verify Git is working correctly in the project directory."""
    
    print("\n🧪 Verifying Git status...")
    
    try:
        result = subprocess.run([
            "git", "status", "--porcelain"
        ], capture_output=True, text=True, check=True, cwd=Path(__file__).parent)
        
        if result.stdout.strip():
            print("📊 Git status output:")
            print(result.stdout)
        else:
            print("✅ Git working directory is clean")
        
        # Also check that Git isn't looking outside the project
        result = subprocess.run([
            "git", "rev-parse", "--show-toplevel"
        ], capture_output=True, text=True, check=True, cwd=Path(__file__).parent)
        
        toplevel = result.stdout.strip()
        project_dir = str(Path(__file__).parent.resolve())
        
        if toplevel.replace('/', '\\').lower() == project_dir.replace('/', '\\').lower():
            print(f"✅ Git repository root correctly set to: {toplevel}")
        else:
            print(f"⚠️  Git repository root mismatch!")
            print(f"   Expected: {project_dir}")
            print(f"   Actual: {toplevel}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error checking Git status: {e}")
        return False
    
    return True

def main():
    """Main function to run all checks and fixes."""
    
    print("=" * 60)
    print("Git User Directory Repository Prevention")
    print("=" * 60)
    
    success = True
    
    # Step 1: Check and fix user Git repository
    if not check_and_fix_user_git_repo():
        success = False
    
    # Step 2: Fix Git safe directories
    if not fix_git_safe_directories():
        success = False
    
    # Step 3: Verify Git status
    if not verify_git_status():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All checks passed! Git is now safe and properly configured.")
    else:
        print("❌ Some issues were found. Please review the output above.")
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    main()
