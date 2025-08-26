"""CodeGeeX4 model plugin for CraftX.py."""

from .base import BaseModelPlugin


class CodeGeeX4(BaseModelPlugin):
    """CodeGeeX4 AI model integration."""

    def __init__(self):
        super().__init__(name="codegeex4", version="1.0.0", ollama_model="codegemma:2b")
        self.description = "CodeGeeX4 - Advanced multilingual code generation model"

    def generate(self, prompt: str, **kwargs) -> str:
        return self.generate_via_providers(prompt, **kwargs)
