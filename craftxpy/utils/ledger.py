from __future__ import annotations

import hashlib
import os
import datetime as _dt


def digest_file(path: str, algo: str = "sha256") -> str:
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return f"{algo}:{h.hexdigest()}"


def append_attestation(
    *,
    ts: str | None = None,
    artifact: str,
    digest: str,
    stage: str,
    model: str | None = None,
    tools: str | None = None,
    inputs: str | None = None,
    ledger_path: str | None = None,
) -> None:
    ts = ts or _dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ")
    ledger_path = ledger_path or os.path.join(os.getcwd(), "ledger", "attestation_ledger.csv")
    os.makedirs(os.path.dirname(ledger_path), exist_ok=True)
    line = ",".join([
        ts,
        artifact,
        digest,
        stage,
        model or "",
        tools or "",
        inputs or "",
    ])
    with open(ledger_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
