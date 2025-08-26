"""CraftX custom model plugin.

Defaults to an Ollama model tag 'davidanderson01/craftx' when available.
Falls back to OpenAI if OPENAI_API_KEY is set and model overridden via env.
"""

from .base import BaseModelPlugin


class CraftXModel(BaseModelPlugin):
    def __init__(self):
        super().__init__(name="craftx", version="1.0.0", ollama_model="davidanderson01/craftx")
        self.description = "CraftX creative and coding model"

    def generate(self, prompt: str, **kwargs) -> str:
        return self.generate_via_providers(prompt, **kwargs)
