from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict

from craftxpy.utils.ledger import append_attestation, digest_file
from craftxpy.utils.tools_registry import get_registry


def _ollama_chat(model: str, messages: list[dict], **kwargs) -> str:
    try:
        import ollama  # type: ignore
    except Exception as e:
        return f"Ollama not available: {e}"
    try:
        out = ollama.chat(model=model, messages=messages)
        return out.get("message", {}).get("content", "")
    except Exception as e:
        return f"Ollama error: {e}"


def route_to_model(input_text: str, *, mode: str = "fast", model: str = "craftx-ml:v1") -> str:
    sys_prompt = (
        "You are CraftX‑ML — a sovereign, multimodal, tool‑orchestrating intelligence."
        " Use concise, practical language and list steps when helpful."
        f" Reasoning mode: {mode}."
    )
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": input_text},
    ]
    return _ollama_chat(model, messages)


def seal_output(input_text: str, output_text: str, *, ledger: str | None = None, model: str = "craftx-ml:v1") -> str:
    # Compute digest of the output bytes
    import hashlib
    h = hashlib.sha256(output_text.encode("utf-8"))
    digest = f"sha256:{h.hexdigest()}"
    append_attestation(
        artifact="craftx-ml-output",
        digest=digest,
        stage="audit",
        model=model,
        tools="|".join(get_registry().keys()),
        inputs="text",
        ledger_path=ledger,
    )
    return digest


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="CraftX Orchestrator")
    p.add_argument("--mode", choices=["fast", "deep", "audit"], default="fast")
    p.add_argument("--input", dest="input_path")
    p.add_argument("--ledger", dest="ledger_path", default=None)
    p.add_argument("--model", dest="model", default="craftx-ml:v1")
    args = p.parse_args(argv)

    text = open(args.input_path, "r", encoding="utf-8").read()
    out = route_to_model(text, mode=args.mode, model=args.model)
    digest = seal_output(text, out, ledger=args.ledger_path, model=args.model)
    print(json.dumps({"output": out, "digest": digest}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
