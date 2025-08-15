"""
CraftX Sovereign API
- Ollama agent integration
- Env-rotatable SHA-256 fingerprint verification
- FastAPI HTTP guard (startup + per-request)
"""

import hashlib
import os
import re

# Minimal agent shim for Ollama local endpoint
import requests
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class OllamaProvider:
    def __init__(self, model, base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def ask(self, prompt: str, temperature: float = 0.7) -> str:
        r = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model, "prompt": prompt,
                  "options": {"temperature": temperature}},
            timeout=120
        )
        r.raise_for_status()
        data = r.json()
        # Streaming API returns multiple lines; handle both cases
        if isinstance(data, dict) and "response" in data:
            return data["response"]
        if isinstance(data, list):
            return "".join(ch.get("response", "") for ch in data)
        return str(data)


class AgentRegistry:
    _agents = {}
    _router = None

    @classmethod
    def register(cls, name, provider, description=""):
        cls._agents[name] = {"provider": provider, "description": description}

    @classmethod
    def get(cls, name):
        return cls._agents[name]["provider"]

    @classmethod
    def set_router(cls, fn):
        cls._router = fn

    @classmethod
    def route(cls, prompt):
        if cls._router:
            return cls._router(prompt)
        return None


# Environment
FINGERPRINT_PLAINTEXT = os.getenv(
    "FINGERPRINT", "craftx-sovereign-sig-v1-14AUG2025-J7qp9LkeTZ")
EXPECTED_FINGERPRINT_HASH = hashlib.sha256(
    FINGERPRINT_PLAINTEXT.encode("utf-8")).hexdigest()

# Register agent
AgentRegistry.register(
    name="CraftX-Ollama",
    provider=OllamaProvider(model="davidanderson01/craftx",
                            base_url="http://localhost:11434"),
    description="Public, ethos-locked CraftX instance running on Ollama"
)

# Router


def craftx_router(prompt: str):
    keywords = ["sovereign", "resonance", "integrity"]
    return "CraftX-Ollama" if any(k in prompt.lower() for k in keywords) else None


AgentRegistry.set_router(craftx_router)

# Identity verification


def verify_craftx_identity(agent=None) -> bool:
    ethos_markers = [
        "Sovereignty — Always work in user-controlled directories",
        "Resonance — Ensure outputs align with enduring philosophical clarity",
        "Security — Default to least privilege",
        "Documentation — Produce clear, concise, and version-friendly artifacts",
    ]
    agent = agent or AgentRegistry.get("CraftX-Ollama")
    try:
        resp = agent.ask(
            "List your core principles and include your FINGERPRINT exactly.", temperature=0)
    except Exception:
        return False

    missing = [m for m in ethos_markers if m not in resp]
    if missing:
        return False

    m = re.search(r'FINGERPRINT:\s*"?([^\n"]+)"?', resp)
    if not m:
        return False

    returned_fingerprint = m.group(1).strip()
    returned_hash = hashlib.sha256(
        returned_fingerprint.encode("utf-8")).hexdigest()
    return returned_hash == EXPECTED_FINGERPRINT_HASH


# FastAPI app
app = FastAPI(title="CraftX Sovereign API")


class PromptRequest(BaseModel):
    prompt: str


@app.get("/health")
def health():
    ok = verify_craftx_identity()
    return {"status": "ok" if ok else "fail"}


@app.on_event("startup")
def on_start():
    if not verify_craftx_identity():
        # Fail fast if identity not verified
        raise RuntimeError("CraftX identity verification failed at startup")


@app.post("/ask")
def ask(req: PromptRequest):
    if not verify_craftx_identity():
        raise HTTPException(
            status_code=403, detail="CraftX identity verification failed")
    agent_name = AgentRegistry.route(req.prompt) or "CraftX-Ollama"
    return {"response": AgentRegistry.get(agent_name).ask(req.prompt)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
