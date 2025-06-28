"""Memory and logging system for CraftX.py."""

import os
import json
from datetime import datetime
from typing import List, Dict, Any


class ChatLogger:
    """Logger for chat sessions and conversation history."""

    def __init__(self, path: str = "chat_logs"):
        """Initialize the chat logger.

        Args:
            path: Directory path to store log files
        """
        self.path = path
        os.makedirs(path, exist_ok=True)

    def save(self, session_id: str, message: str, role: str = "user") -> None:
        """Save a message to the chat log.

        Args:
            session_id: Unique identifier for the chat session
            message: The message content
            role: The role of the message sender ('user' or 'assistant')
        """
        filename = os.path.join(self.path, f"{session_id}.json")
        entry = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "message": message
        }

        # Load existing data or create new list
        data = []
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, IOError):
                data = []

        # Append new entry and save
        data.append(entry)
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"⚠️ Failed to save chat log: {e}")

    def load(self, session_id: str) -> List[Dict[str, Any]]:
        """Load chat history for a session.

        Args:
            session_id: The session identifier

        Returns:
            List of message entries
        """
        filename = os.path.join(self.path, f"{session_id}.json")
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def list_sessions(self) -> List[str]:
        """List all available chat sessions.

        Returns:
            List of session IDs
        """
        sessions = []
        for filename in os.listdir(self.path):
            if filename.endswith(".json"):
                sessions.append(filename[:-5])  # Remove .json extension
        return sorted(sessions)

    def delete_session(self, session_id: str) -> bool:
        """Delete a chat session.

        Args:
            session_id: The session to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        filename = os.path.join(self.path, f"{session_id}.json")
        try:
            if os.path.exists(filename):
                os.remove(filename)
                return True
        except IOError:
            pass
        return False
