"""Secure shell execution utilities for CraftX.py."""

import subprocess
from typing import List

# Whitelist of safe commands for secure execution
WHITELIST: List[str] = [
    "whoami", "ls", "dir", "echo", "ipconfig", "ifconfig",
    "hostname", "pwd", "date", "time", "uname", "systeminfo"
]


def run_safe_command(cmd: str) -> str:
    """Execute a command safely using a whitelist approach.

    Args:
        cmd: The command string to execute

    Returns:
        Command output or error message
    """
    if not cmd.strip():
        return "❌ Empty command"

    # Extract the base command (first word)
    base_command = cmd.split()[0]

    if base_command not in WHITELIST:
        return f"❌ Command `{base_command}` not allowed. Allowed commands: {', '.join(WHITELIST)}"

    try:
        result = subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.STDOUT,
            timeout=5,
            text=True
        )
        return result.strip()
    except subprocess.TimeoutExpired:
        return "⚠️ Command timed out after 5 seconds"
    except subprocess.CalledProcessError as e:
        return f"⚠️ Command failed with exit code {e.returncode}: {e.output}"
    except (OSError, FileNotFoundError) as e:
        return f"⚠️ Command execution error: {str(e)}"


def add_safe_command(command: str) -> bool:
    """Add a command to the whitelist.

    Args:
        command: The command to add

    Returns:
        True if added successfully, False if already exists
    """
    if command not in WHITELIST:
        WHITELIST.append(command)
        return True
    return False


def remove_safe_command(command: str) -> bool:
    """Remove a command from the whitelist.

    Args:
        command: The command to remove

    Returns:
        True if removed successfully, False if not found
    """
    if command in WHITELIST:
        WHITELIST.remove(command)
        return True
    return False


def get_safe_commands() -> List[str]:
    """Get the current list of safe commands.

    Returns:
        List of whitelisted commands
    """
    return WHITELIST.copy()
