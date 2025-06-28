"""Base plugin interface for CraftX.py model integrations."""


class BaseModelPlugin:
    """Base class for all AI model plugins in CraftX.py."""

    def __init__(self):
        self.model_name = self.__class__.__name__

    def generate(self, prompt: str) -> str:
        """Generate a response from the model given a prompt.

        Args:
            prompt: The input prompt string

        Returns:
            Generated response string

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Must implement generate() method")

    def get_model_info(self) -> dict:
        """Get information about this model plugin.

        Returns:
            Dictionary containing model metadata
        """
        return {
            "name": self.model_name,
            "version": getattr(self, "version", "unknown"),
            "description": getattr(self, "description", "No description available")
        }
