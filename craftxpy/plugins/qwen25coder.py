"""Qwen2.5-Coder model plugin for CraftX.py."""

from .base import BaseModelPlugin


class Qwen25Coder(BaseModelPlugin):
    """Qwen2.5-Coder AI model integration."""

    def __init__(self):
        super().__init__(name="qwen25coder", version="1.0.0",
                         ollama_model="qwen2.5-coder:1.5b")
        self.description = "Qwen2.5-Coder - State-of-the-art code generation model"

    def generate(self, prompt: str, **kwargs) -> str:
        return self.generate_via_providers(prompt, **kwargs)
