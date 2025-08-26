"""CraftX.py Base Plugin Module

Base plugin classes and plugin system for extensible AI assistants.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import os


class BasePlugin(ABC):
    """Base class for all CraftX.py plugins."""

    def __init__(self, name: str, version: str = "1.0.0"):
        """Initialize the plugin.

        Args:
            name: Plugin name
            version: Plugin version
        """
        self.name = name
        self.version = version
        self.enabled = True
        self.config: Dict[str, Any] = {}

    @abstractmethod
    def execute(self, input_data: Any, **kwargs) -> Any:
        """Execute the plugin functionality.

        Args:
            input_data: Input data to process
            **kwargs: Additional parameters

        Returns:
            Processed output
        """
        raise NotImplementedError("Subclasses must implement process method")

    def configure(self, config: Dict[str, Any]) -> None:
        """Configure the plugin.

        Args:
            config: Configuration dictionary
        """
        self.config.update(config)

    def enable(self) -> None:
        """Enable the plugin."""
        self.enabled = True

    def disable(self) -> None:
        """Disable the plugin."""
        self.enabled = False

    def get_info(self) -> Dict[str, Any]:
        """Get plugin information.

        Returns:
            Plugin information dictionary
        """
        return {
            "name": self.name,
            "version": self.version,
            "enabled": self.enabled,
            "config": self.config
        }


class BaseModelPlugin(BasePlugin):
    """Base class for model-backed plugins.

    Provides provider-agnostic helpers to call Ollama (local) or OpenAI.
    Subclasses should set default model names or rely on env var overrides.
    """

    def __init__(self, name: str, version: str = "1.0.0", *,
                 ollama_model: Optional[str] = None,
                 openai_model: Optional[str] = None):
        super().__init__(name=name, version=version)
        self.ollama_model = ollama_model
        self.openai_model = openai_model

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError

    # Provide a default execute() implementation to satisfy BasePlugin
    # type: ignore[override]
    def execute(self, input_data: Any, **kwargs) -> Any:
        prompt = str(input_data) if input_data is not None else ""
        return self.generate(prompt, **kwargs)

    # -------- Provider helpers --------
    def _generate_via_ollama(self, prompt: str, **kwargs) -> Optional[str]:
        model = (
            os.environ.get(
                f"CRAFTX_MODEL_{self.name.upper().replace('-', '_')}_OLLAMA")
            or os.environ.get("CRAFTX_OLLAMA_MODEL")
            or self.ollama_model
            or "llama3.1"
        )
        try:
            import ollama  # type: ignore
        except Exception:
            return None
        try:
            resp = ollama.chat(model=model, messages=[
                               {"role": "user", "content": prompt}])
            return resp.get("message", {}).get("content") or ""
        except Exception:
            return None

    def _generate_via_openai(self, prompt: str, **kwargs) -> Optional[str]:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return None
        model = (
            os.environ.get(
                f"CRAFTX_MODEL_{self.name.upper().replace('-', '_')}_OPENAI")
            or self.openai_model
            or "gpt-4o-mini"
        )
        temperature = float(kwargs.get("temperature", 0.7))
        max_tokens = int(kwargs.get("max_tokens", 512))
        try:
            from openai import OpenAI  # type: ignore
            client = OpenAI()
            out = client.chat.completions.create(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return out.choices[0].message.content if out.choices else ""
        except Exception:
            return None

    def generate_via_providers(self, prompt: str, **kwargs) -> str:
        """Try Ollama first, then OpenAI. Return informative error if none available."""
        text = self._generate_via_ollama(prompt, **kwargs)
        if text:
            return text
        text = self._generate_via_openai(prompt, **kwargs)
        if text:
            return text
        return (
            "No LLM provider available. Install and run Ollama or set OPENAI_API_KEY.\n"
            "- Ollama: https://ollama.com (set CRAFTX_OLLAMA_MODEL to choose a model)\n"
            "- OpenAI: set OPENAI_API_KEY and optional model via CRAFTX_MODEL_<PLUGIN>_OPENAI"
        )

    # -------- Conversation helpers --------
    def _chat_via_ollama(self, messages: list[dict], **kwargs) -> Optional[str]:
        model = (
            os.environ.get(
                f"CRAFTX_MODEL_{self.name.upper().replace('-', '_')}_OLLAMA")
            or os.environ.get("CRAFTX_OLLAMA_MODEL")
            or self.ollama_model
            or "llama3.1"
        )
        try:
            import ollama  # type: ignore
        except Exception:
            return None
        try:
            resp = ollama.chat(model=model, messages=messages)
            return resp.get("message", {}).get("content") or ""
        except Exception:
            return None

    def _chat_via_openai(self, messages: list[dict], **kwargs) -> Optional[str]:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return None
        model = (
            os.environ.get(
                f"CRAFTX_MODEL_{self.name.upper().replace('-', '_')}_OPENAI")
            or self.openai_model
            or "gpt-4o-mini"
        )
        temperature = float(kwargs.get("temperature", 0.7))
        max_tokens = int(kwargs.get("max_tokens", 512))
        try:
            from openai import OpenAI  # type: ignore
            client = OpenAI()
            out = client.chat.completions.create(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=messages,
            )
            return out.choices[0].message.content if out.choices else ""
        except Exception:
            return None

    def generate_chat_via_providers(self, messages: list[dict], **kwargs) -> str:
        text = self._chat_via_ollama(messages, **kwargs)
        if text:
            return text
        text = self._chat_via_openai(messages, **kwargs)
        if text:
            return text
        return (
            "No LLM provider available. Install and run Ollama or set OPENAI_API_KEY.\n"
            "- Ollama: https://ollama.com (set CRAFTX_OLLAMA_MODEL to choose a model)\n"
            "- OpenAI: set OPENAI_API_KEY and optional model via CRAFTX_MODEL_<PLUGIN>_OPENAI"
        )


class DemoPlugin(BasePlugin):
    """Demo plugin for testing purposes."""

    def __init__(self):
        """Initialize the demo plugin."""
        super().__init__("Demo Plugin", "0.1.2")

    def execute(self, input_data: Any, **kwargs) -> str:
        """Execute demo functionality.

        Args:
            input_data: Input data
            **kwargs: Additional parameters

        Returns:
            Demo response
        """
        return f"Demo plugin processed: {input_data}"
