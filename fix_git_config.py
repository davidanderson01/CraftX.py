#!/usr/bin/env python3
"""
Git Configuration Cleanup Script
Fixes sparse checkout, line ending warnings, and Git configuration issues.
"""

# import sys
import os
import subprocess


def run_git_command(command, description):
    """Run a git command and handle errors."""
    try:
        print(f"🔧 {description}...")
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, cwd=os.getcwd(), check=False
        )
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"⚠️  {description} had warnings: {result.stderr.strip()}")
        return result.returncode == 0
    except (subprocess.SubprocessError, OSError) as e:
        print(f"❌ Error running {description}: {e}")
        return False


def main():
    print("🚀 Git Configuration Cleanup")
    print("=" * 50)

    # 1. Disable sparse checkout warnings
    run_git_command(
        "git config advice.updateSparsePath false",
        "Disabling sparse checkout warnings"
    )

    # 2. Configure line endings for cross-platform compatibility
    run_git_command(
        "git config core.autocrlf true",
        "Setting line ending conversion to auto"
    )

    # 3. Disable line ending warnings
    run_git_command(
        "git config core.safecrlf false",
        "Disabling line ending warnings"
    )

    # 4. Check if sparse checkout is enabled
    result = subprocess.run(
        "git config core.sparseCheckout", shell=True, capture_output=True, text=True, check=False
    )
    if result.returncode == 0 and result.stdout.strip().lower() == "true":
        print("📋 Sparse checkout is enabled")

        # 5. Disable sparse checkout to include all files
        choice = input(
            "Would you like to disable sparse checkout to include all files? (y/n): "
        ).lower()
        if choice == 'y':
            run_git_command(
                "git config core.sparseCheckout false",
                "Disabling sparse checkout"
            )
            run_git_command(
                "git read-tree -m -u HEAD",
                "Updating working directory to include all files"
            )
    else:
        print("📋 Sparse checkout is not enabled")

    # 6. Clean up untracked Azure Functions files
    print("\n🧹 Cleaning up Azure Functions files...")
    if os.path.exists(".azure-functions-core-tools"):
        run_git_command(
            "git clean -fd .azure-functions-core-tools/",
            "Removing Azure Functions Core Tools directory"
        )

    # 7. Add updated .gitignore
    run_git_command(
        "git add .gitignore",
        "Adding updated .gitignore file"
    )

    # 8. Show current Git status
    print("\n📊 Current Git Status:")
    subprocess.run("git status --short", shell=True)

    print("\n✨ Git configuration cleanup completed!")
    print("\nNext steps:")
    print("1. Review the current status above")
    print("2. Commit your changes: git commit -m 'Update .gitignore and fix Git config'")
    print("3. Push to remote: git push origin main")


if __name__ == "__main__":
    main()
