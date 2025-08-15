craftx-stack

This folder contains the craftx sovereign bundle.

Quick notes:

- Secrets have been moved to `secrets/` inside this folder. Do not commit them. Use `.env.template` and `Private Key.env.template` as placeholders.
- Useful tools copied from the dropped folder are under `tools/` (e.g. `wallet-gen`, `ethverify` source).
- A small Python verifier is available at `scripts/verify_eth.py`.

To deploy the attestation contract (example):

1. Install Python deps:

```powershell
python -m pip install -r requirements.txt
```

2. Populate `.env` in this folder (or copy from `secrets/.env` locally) and run:

```powershell
python scripts/deploy_contract.py
```

3. Build and run containers:

```powershell
docker compose up -d --build
```

Cleanup performed by the assistant:

- Moved secrets into `secrets/`.
- Removed compiled `bin/` and `obj/` folders from the dropped folder.
- Created `.gitignore` entries to prevent committing binaries and secrets.

If you want me to further:

- Reimplement dotnet verifier in Python and wire into attester container.
- Create a dotnet Dockerfile for the verifier.
- Remove the dropped folder entirely (you asked to keep it until final review).

Tell me which follow-ups to run.
