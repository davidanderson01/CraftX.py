"""
craftx.py — Sovereign Orchestrator for CraftX‑ML

Modular command interface, tool router, and attestation logger.
Created: 2025-08-23

Features:
- Wire to CraftX‑ML via Ollama (local)
- Tool registry integration (hash_file, docker_deploy, field_log, image_describe)
- Input parsing: text, JSON, image, audio, simple CSV/MD
- Reasoning modes: fast, deep, audit
- Attestation: SHA‑256 digest + CSV ledger entry
- Optional: self-seal fingerprint entry

CLI examples (PowerShell):
  # Simple text
  python .\craftx.py --text "Plan a secure rollout for v2"

  # From file
  python .\craftx.py --input .\docs\intro.md --mode deep

  # Run a tool explicitly
  python .\craftx.py --tool hash_file --tool-args '{"path": "README.md"}'

  # Seal this orchestrator itself in the ledger
  python .\craftx.py --seal-self
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

# Local utilities
from craftxpy.utils.ledger import append_attestation
from craftxpy.utils.tools_registry import get_registry, Tool


# ---------------- Configuration ----------------
DEFAULT_MODEL = os.getenv("CRAFTX_MODEL", "craftx-ml:v1")
LEDGER_PATH = os.getenv("CRAFTX_LEDGER", str(
    Path.cwd() / "ledger" / "attestation_ledger.csv"))


# ---------------- Model Routing ----------------
def _ollama_chat(model: str, messages: list[dict]) -> str:
    """Call Ollama chat; returns assistant content or error message.

    Falls back to HTTP if the Python client is not available.
    """
    try:
        import ollama  # type: ignore
        out = ollama.chat(model=model, messages=messages)
        return out.get("message", {}).get("content", "")
    except Exception:
        # HTTP fallback (best-effort)
        import requests
        url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
        payload = {"model": model, "messages": messages, "stream": False}
        try:
            r = requests.post(url, json=payload, timeout=180)
            r.raise_for_status()
            data = r.json()
            # Newer chat API returns {message: {role, content}}
            if isinstance(data, dict) and "message" in data:
                return data["message"].get("content", "")
            # generate API compatibility
            return data.get("response") or json.dumps(data)
        except Exception as e:
            return f"Ollama error: {e}"


def _build_system_prompt(mode: str, defense: bool) -> str:
    base = (
        "You are CraftX‑ML — a sovereign, multimodal, tool‑orchestrating intelligence. "
        "Be concise and actionable. When useful, present steps and edge cases."
    )
    mode_line = f" Reasoning mode: {mode}."
    defense_line = (
        " Defense mode enabled: prioritize IOC detection, anomaly heuristics, and safe guidance."
        if defense
        else ""
    )
    return base + mode_line + defense_line


def route_to_model(prompt: str, *, mode: str = "fast", model: str = DEFAULT_MODEL, defense: bool = False) -> str:
    sys_prompt = _build_system_prompt(mode, defense)
    tagged = f"[{mode.upper()} MODE]\n{prompt}" if mode else prompt
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": tagged},
    ]
    return _ollama_chat(model, messages)


# ---------------- Tool Routing ----------------
def list_tools() -> Dict[str, Tool]:
    return get_registry()


def run_tool(name: str, kwargs: Dict[str, Any] | None = None) -> Tuple[str, Optional[str]]:
    """Run a registered tool by name with kwargs.

    Returns (result_string, error_string_or_None)
    """
    registry = list_tools()
    tool = registry.get(name)
    if not tool:
        return "", f"Unknown tool: {name}"
    try:
        res = tool.func(**(kwargs or {}))
        # Ensure string for output
        if not isinstance(res, str):
            try:
                res = json.dumps(res, ensure_ascii=False)
            except Exception:
                res = str(res)
        return res, None
    except TypeError as e:
        return "", f"Argument error for {name}: {e}"
    except Exception as e:
        return "", f"Tool error for {name}: {e}"


# ---------------- Input Parsing ----------------
@dataclass
class ParsedInput:
    kind: str  # text|structured|image|audio|unknown
    content: str  # text content or descriptor
    aux: Dict[str, Any]


def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")


def parse_input(src: str) -> ParsedInput:
    """Parse an input source:
    - If file path exists, detect by extension.
    - Else treat as raw text; if it looks like JSON, mark as structured.
    """
    path = Path(src)
    if path.exists() and path.is_file():
        ext = path.suffix.lower()
        if ext in {".txt", ".md", ".py", ".yaml", ".yml", ".csv"}:
            return ParsedInput("text", _read_text(path), {"path": str(path), "ext": ext})
        if ext in {".json"}:
            try:
                data = json.loads(_read_text(path))
                return ParsedInput("structured", json.dumps(data, ensure_ascii=False), {"path": str(path), "ext": ext})
            except Exception:
                return ParsedInput("text", _read_text(path), {"path": str(path), "ext": ext, "note": "json-parse-failed"})
        if ext in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
            # Use image_describe tool if available
            desc, err = run_tool("image_describe", {"path": str(path)})
            content = desc if not err else f"[IMAGE INPUT] {path.name} ({err})"
            return ParsedInput("image", content, {"path": str(path), "ext": ext})
        if ext in {".wav", ".mp3", ".m4a", ".flac", ".ogg"}:
            # Light stub: rely on external transcriber if present later
            return ParsedInput("audio", f"[AUDIO INPUT] {path.name}", {"path": str(path), "ext": ext})
        # Fallback
        return ParsedInput("unknown", f"[UNKNOWN INPUT] {str(path)}", {"path": str(path), "ext": ext})

    # Not a file — treat as text; try JSON detection
    raw = src.strip()
    if (raw.startswith("{") and raw.endswith("}")) or (raw.startswith("[") and raw.endswith("]")):
        try:
            data = json.loads(raw)
            return ParsedInput("structured", json.dumps(data, ensure_ascii=False), {})
        except Exception:
            pass
    return ParsedInput("text", raw, {})


# ---------------- Attestation ----------------
def sha256_text(t: str) -> str:
    h = hashlib.sha256()
    h.update(t.encode("utf-8"))
    return f"sha256:{h.hexdigest()}"


def log_attestation(*, artifact: str, digest: str, stage: str, model: Optional[str] = None, tools: Optional[str] = None, inputs: Optional[str] = None, ledger_path: Optional[str] = None) -> None:
    append_attestation(
        artifact=artifact,
        digest=digest,
        stage=stage,
        model=model,
        tools=tools,
        inputs=inputs,
        ledger_path=ledger_path or LEDGER_PATH,
    )


def seal_self(file_path: str) -> str:
    """Compute this file's SHA‑256 and write a ledger entry."""
    p = Path(file_path)
    digest = ""
    try:
        h = hashlib.sha256()
        with p.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        digest = f"sha256:{h.hexdigest()}"
        log_attestation(
            artifact=p.name,
            digest=digest,
            stage="sealed",
            model=DEFAULT_MODEL,
            tools="|".join(list_tools().keys()),
            inputs="orchestrator",
        )
    except Exception as e:
        digest = f"error:{e}"
    return digest


# ---------------- Orchestration ----------------
def build_prompt(parsed: ParsedInput) -> str:
    if parsed.kind == "structured":
        return f"[STRUCTURED INPUT]\n{parsed.content}"
    if parsed.kind == "image":
        return f"[VISION]\n{parsed.content}"
    if parsed.kind == "audio":
        return f"[AUDIO]\n{parsed.content}"
    return parsed.content


def orchestrate(
    source: str,
    *,
    mode: str = "fast",
    model: str = DEFAULT_MODEL,
    defense: bool = False,
    ledger_path: Optional[str] = None,
) -> Dict[str, Any]:
    parsed = parse_input(source)
    prompt = build_prompt(parsed)
    output = route_to_model(prompt, mode=mode, model=model, defense=defense)
    digest = sha256_text(output)
    log_attestation(
        artifact="craftx-ml-output",
        digest=digest,
        stage=mode,
        model=model,
        tools="|".join(list_tools().keys()),
        inputs=parsed.kind,
        ledger_path=ledger_path,
    )
    return {"output": output, "digest": digest, "kind": parsed.kind}


def orchestrate_tool(name: str, kwargs: Dict[str, Any] | None = None, *, ledger_path: Optional[str] = None) -> Dict[str, Any]:
    result, err = run_tool(name, kwargs or {})
    digest = sha256_text(result if result else (err or ""))
    log_attestation(
        artifact=f"tool:{name}",
        digest=digest,
        stage="tool",
        model=DEFAULT_MODEL,
        tools=name,
        inputs="kwargs-json",
        ledger_path=ledger_path,
    )
    return {"tool": name, "result": result, "error": err, "digest": digest}


# ---------------- CLI ----------------
def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="CraftX Sovereign Orchestrator")
    src = p.add_mutually_exclusive_group(required=False)
    src.add_argument(
        "--input", help="Path to input file (text/json/image/audio)")
    src.add_argument("--text", help="Raw text or JSON string input")
    p.add_argument("--mode", choices=["fast", "deep", "audit"], default="fast")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--ledger", help="Override ledger CSV path", default=None)
    p.add_argument("--defense", action="store_true",
                   help="Enable defense posture")

    # Tool execution
    p.add_argument(
        "--tool", help="Run a specific tool by name (e.g., hash_file)")
    p.add_argument(
        "--tool-args", help="JSON object of kwargs for the tool", default=None)

    # Utilities
    p.add_argument("--list-tools", action="store_true",
                   help="List available tools")
    p.add_argument("--seal-self", action="store_true",
                   help="Seal craftx.py fingerprint to ledger")
    return p


def main(argv: Optional[list[str]] = None) -> int:
    args = _build_argparser().parse_args(argv)

    if args.list_tools:
        registry = list_tools()
        names = sorted(registry.keys())
        print(json.dumps({"tools": names}, ensure_ascii=False))
        return 0

    if args.seal_self:
        digest = seal_self(__file__)
        print(json.dumps({"artifact": Path(__file__).name,
              "digest": digest}, ensure_ascii=False))
        # Exit early if no other operation requested
        if not (args.tool or args.input or args.text or args.list_tools):
            return 0

    # Tool path wins if specified
    if args.tool:
        kwargs = {}
        if args.tool_args:
            try:
                kwargs = json.loads(args.tool_args)
            except Exception as e:
                print(json.dumps(
                    {"error": f"Invalid --tool-args JSON: {e}"}, ensure_ascii=False))
                return 2
        result = orchestrate_tool(args.tool, kwargs, ledger_path=args.ledger)
        print(json.dumps(result, ensure_ascii=False))
        return 0 if not result.get("error") else 1

    # Orchestration path
    if not args.input and not args.text:
        print(json.dumps(
            {"error": "Provide --input file or --text"}, ensure_ascii=False))
        return 2

    source = args.input if args.input else args.text
    result = orchestrate(
        source or "",
        mode=args.mode,
        model=args.model,
        defense=args.defense,
        ledger_path=args.ledger,
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
