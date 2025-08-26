"""CraftX-ML Tools Registry

Lightweight registry of callable tools exposed to the assistant orchestration.
Includes attestation helpers and deployment/logging stubs.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Any
import hashlib
import subprocess
import datetime as _dt
import json
import os


@dataclass
class Tool:
    name: str
    func: Callable[..., Any]
    description: str


def hash_file(path: str, algo: str = "sha256") -> str:
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return f"{algo}:{h.hexdigest()}"


def docker_deploy(image: str, *, container_name: str | None = None) -> str:
    # Minimal stub; real-world version would accept env, ports, volumes, etc.
    container_name = container_name or f"craftx-{int(_dt.datetime.utcnow().timestamp())}"
    cmd = ["docker", "run", "-d", "--name", container_name, image]
    try:
        out = subprocess.check_output(cmd, text=True)
        return out.strip()
    except Exception as e:
        return f"docker_deploy error: {e}"


def field_log(event: str, *, meta: Dict[str, Any] | None = None, ledger_path: str | None = None) -> str:
    meta = meta or {}
    ledger_path = ledger_path or os.path.join(
        os.getcwd(), "ledger", "field_log.jsonl")
    os.makedirs(os.path.dirname(ledger_path), exist_ok=True)
    rec = {
        "ts": _dt.datetime.utcnow().isoformat() + "Z",
        "event": event,
        "meta": meta,
    }
    with open(ledger_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
    return "logged"


def image_describe(path: str) -> str:
    # Placeholder: real impl would send image to a vision model and return a caption/analysis
    return f"Describe image at {path}: (vision model integration pending)"


def get_registry() -> Dict[str, Tool]:
    return {
        "hash_file": Tool("hash_file", hash_file, "Return SHA hash for a file path."),
        "docker_deploy": Tool("docker_deploy", docker_deploy, "Run a Docker container in detached mode."),
        "field_log": Tool("field_log", field_log, "Append an event to the field log ledger."),
        "image_describe": Tool("image_describe", image_describe, "Describe an image using a vision model."),
    }
