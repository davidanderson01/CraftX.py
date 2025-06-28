"""Agent routing system for CraftX.py."""

from typing import Dict, Any, Optional
from ..plugins.base import BaseModelPlugin


class AgentRouter:
    """Router for managing and dispatching tasks to different AI models."""

    def __init__(self, models: Optional[Dict[str, BaseModelPlugin]] = None):
        """Initialize the agent router.

        Args:
            models: Dictionary mapping task types to model instances
        """
        self.models = models or {}

    def route(self, task_type: str, prompt: str) -> str:
        """Route a task to the appropriate model.

        Args:
            task_type: The type of task to perform
            prompt: The input prompt for the task

        Returns:
            Generated response from the appropriate model
        """
        model = self.models.get(task_type)
        if not model:
            return f"❌ No model registered for task type '{task_type}'"

        try:
            return model.generate(prompt)
        except (AttributeError, TypeError) as e:
            return f"❌ Model error: {str(e)}"
        except (ImportError, ModuleNotFoundError) as e:
            return f"❌ Model dependency error: {str(e)}"
        except (RuntimeError, ValueError) as e:
            return f"❌ Error generating response: {str(e)}"

    def register(self, task_type: str, model: BaseModelPlugin) -> None:
        """Register a model for a specific task type.

        Args:
            task_type: The task type identifier
            model: The model plugin instance
        """
        self.models[task_type] = model

    def unregister(self, task_type: str) -> bool:
        """Unregister a model for a task type.

        Args:
            task_type: The task type to unregister

        Returns:
            True if model was found and removed, False otherwise
        """
        if task_type in self.models:
            del self.models[task_type]
            return True
        return False

    def list_models(self) -> Dict[str, Dict[str, Any]]:
        """List all registered models and their information.

        Returns:
            Dictionary of task types mapped to model information
        """
        return {
            task_type: model.get_model_info()
            for task_type, model in self.models.items()
        }
