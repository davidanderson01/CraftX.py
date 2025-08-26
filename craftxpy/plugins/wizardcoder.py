"""WizardCoder model plugin for CraftX.py."""

from .base import BaseModelPlugin


class WizardCoder(BaseModelPlugin):
    """WizardCoder AI model integration."""

    def __init__(self):
        super().__init__(name="wizardcoder", version="1.0.0", ollama_model="wizardcoder:7b")
        self.description = "WizardCoder - Advanced code generation model"

    def generate(self, prompt: str, **kwargs) -> str:
        return self.generate_via_providers(prompt, **kwargs)
