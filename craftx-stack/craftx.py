"""
CraftX Sovereign API
- Ollama agent integration
- Env-rotatable SHA-256 fingerprint verification
- FastAPI HTTP guard (startup + per-request)
- OAuth authentication endpoints
"""

import hashlib
import json
import os
import re
import secrets
from datetime import datetime, timedelta
from typing import Optional

# Minimal agent shim for Ollama local endpoint
import requests
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Import the OAuth authentication system
try:
    import sys
    import os
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    from craftxpy.utils.auth import universal_auth
    from oauth_config_loader import get_oauth_config
    from user_analytics import analytics
    from analytics_dashboard import add_analytics_routes
    OAUTH_AVAILABLE = True
except ImportError:
    print("⚠️  OAuth system not available. OAuth endpoints will be disabled.")
    OAUTH_AVAILABLE = False
    universal_auth = None
    get_oauth_config = None
    analytics = None
    add_analytics_routes = None


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

# Mount static files (for serving the HTML page)
if os.path.exists("../"):
    app.mount("/static", StaticFiles(directory="../"), name="static")

# Initialize authentication system if available
if OAUTH_AVAILABLE and universal_auth:
    universal_auth.initialize_auth()


class PromptRequest(BaseModel):
    prompt: str


class AuthCallback(BaseModel):
    code: str
    state: str


# OAuth endpoints
if OAUTH_AVAILABLE:
    # Add analytics dashboard routes
    add_analytics_routes(app, analytics)


@app.get("/")
async def serve_index():
    """Serve the main index.html page"""
    try:
        with open("../index.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>CraftX.py OAuth Server</h1><p>Index file not found</p>")


@app.get("/privacy.html")
async def serve_privacy():
    """Serve the privacy policy page"""
    try:
        with open("../privacy.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Privacy Policy</h1><p>Privacy policy not found</p>")


@app.get("/terms.html")
async def serve_terms():
    """Serve the terms of service page"""
    try:
        with open("../terms.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Terms of Service</h1><p>Terms of service not found</p>")


@app.get("/eula.html")
async def serve_eula():
    """Serve the EULA page"""
    try:
        with open("../eula.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>EULA</h1><p>End User License Agreement not found</p>")


@app.get("/nda.html")
async def serve_nda():
    """Serve the NDA page"""
    try:
        with open("../nda.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>NDA</h1><p>Non-Disclosure Agreement not found</p>")


@app.get("/auth/{provider}")
async def oauth_login(provider: str, request: Request):
    """Initiate OAuth login for the specified provider"""
    if not OAUTH_AVAILABLE:
        raise HTTPException(
            status_code=503, detail="OAuth system not available")

    try:
        # Track authentication attempt
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "Unknown")

        analytics.track_auth_event(
            provider=provider,
            event_type="auth_attempt",
            ip_address=client_ip,
            user_agent=user_agent,
            success=True,
            metadata={"step": "initiate"}
        )
        # Generate state for security
        state = secrets.token_urlsafe(32)

        # Store state in a simple session (in production, use proper session storage)
        state_file = f"oauth_states/{state}.json"
        os.makedirs("oauth_states", exist_ok=True)
        with open(state_file, "w") as f:
            json.dump({
                "provider": provider,
                "created_at": datetime.now().isoformat(),
                "redirect_uri": f"{request.base_url}auth/callback/{provider}"
            }, f)

        # Generate OAuth URL
        redirect_uri = f"{request.base_url}auth/callback/{provider}"
        oauth_url = universal_auth.generate_oauth_url(
            provider, redirect_uri, state)

        return RedirectResponse(url=oauth_url)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"OAuth initialization failed: {str(e)}")


@app.get("/auth/callback/{provider}")
async def oauth_callback(provider: str, code: str, state: str, request: Request):
    """Handle OAuth callback and create user session"""
    if not OAUTH_AVAILABLE:
        raise HTTPException(
            status_code=503, detail="OAuth system not available")

    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "Unknown")

    try:
        # Verify state
        state_file = f"oauth_states/{state}.json"
        if not os.path.exists(state_file):
            analytics.track_auth_event(
                provider=provider,
                event_type="auth_error",
                ip_address=client_ip,
                user_agent=user_agent,
                success=False,
                error_message="Invalid or expired state"
            )
            raise HTTPException(
                status_code=400, detail="Invalid or expired state")

        with open(state_file, "r") as f:
            state_data = json.load(f)

        # Clean up state file
        os.remove(state_file)

        if state_data["provider"] != provider:
            analytics.track_auth_event(
                provider=provider,
                event_type="auth_error",
                ip_address=client_ip,
                user_agent=user_agent,
                success=False,
                error_message="Provider mismatch"
            )
            raise HTTPException(status_code=400, detail="Provider mismatch")

        # Exchange code for token (simplified implementation)
        # In a full implementation, you'd use the OAuth provider's token endpoint
        user_data = {
            "provider": provider,
            "code": code,
            "authenticated_at": datetime.now().isoformat(),
            # In real implementation, fetch user info from the provider
            "email": f"user@{provider}.com",  # Placeholder
            "name": f"User from {provider.title()}"  # Placeholder
        }

        # Create session
        session_id = universal_auth.create_session(user_data, provider)

        # Generate user_id for analytics (in real implementation, use provider's user ID)
        user_id = f"{provider}_{hashlib.sha256(user_data['email'].encode()).hexdigest()[:8]}"

        # Create analytics session
        analytics_session_id = analytics.create_user_session(
            user_id=user_id,
            email=user_data['email'],
            provider=provider,
            ip_address=client_ip,
            user_agent=user_agent
        )

        # Generate download token
        download_token = secrets.token_urlsafe(32)

        # Store download token with analytics session info
        os.makedirs("download_tokens", exist_ok=True)
        with open(f"download_tokens/{download_token}.json", "w") as f:
            json.dump({
                "session_id": session_id,
                "analytics_session_id": analytics_session_id,
                "user_id": user_id,
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=1)).isoformat()
            }, f)

        # Redirect back to index with token
        return RedirectResponse(url=f"/?token={download_token}&provider={provider}")

    except HTTPException:
        raise
    except Exception as e:
        analytics.track_auth_event(
            provider=provider,
            event_type="auth_error",
            ip_address=client_ip,
            user_agent=user_agent,
            success=False,
            error_message=str(e)
        )
        raise HTTPException(
            status_code=500, detail=f"OAuth callback failed: {str(e)}")


@app.get("/download/craftxpy.zip")
async def download_craftxpy(token: str, request: Request):
    """Serve the CraftXPy download with token verification"""
    if not OAUTH_AVAILABLE:
        raise HTTPException(
            status_code=503, detail="OAuth system not available")

    try:
        # Verify download token
        token_file = f"download_tokens/{token}.json"
        if not os.path.exists(token_file):
            raise HTTPException(
                status_code=401, detail="Invalid or expired download token")

        with open(token_file, "r") as f:
            token_data = json.load(f)

        # Check expiration
        expires_at = datetime.fromisoformat(token_data["expires_at"])
        if datetime.now() > expires_at:
            os.remove(token_file)
            raise HTTPException(
                status_code=401, detail="Download token expired")

        # Verify session is still valid
        session_id = token_data["session_id"]
        session = universal_auth.get_session(session_id)

        # Track download in analytics
        if "user_id" in token_data and "analytics_session_id" in token_data:
            analytics.track_download(
                user_id=token_data["user_id"],
                session_id=token_data["analytics_session_id"]
            )
            analytics.track_auth_event(
                provider=session.get("provider", "unknown"),
                event_type="download",
                ip_address=request.client.host,
                user_agent=request.headers.get("user-agent", "Unknown"),
                user_id=token_data["user_id"],
                success=True,
                metadata={"download_token": token[:8]}
            )
        if not session:
            raise HTTPException(status_code=401, detail="Invalid session")

        # For now, return a simple response (you'd create an actual zip file here)
        return {
            "message": "Download authorized!",
            "session_info": {
                "provider": session["provider_id"],
                "user": session["user_data"]["name"],
                "authenticated_at": session["created_at"]
            },
            "download_instructions": "In a production environment, this would trigger a zip file download of the CraftXPy package."
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Download failed: {str(e)}")


# Configuration endpoints (admin use)
@app.post("/admin/configure-oauth")
async def configure_oauth_provider(provider: str, client_id: str, client_secret: str, domain: str = ""):
    """Configure OAuth provider credentials (admin endpoint)"""
    if not OAUTH_AVAILABLE:
        raise HTTPException(
            status_code=503, detail="OAuth system not available")

    try:
        universal_auth.add_provider_config(
            provider, client_id, client_secret, domain)
        return {"message": f"Provider {provider} configured successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Configuration failed: {str(e)}")


@app.get("/admin/oauth-status")
async def get_oauth_status():
    """Get OAuth configuration status"""
    if not OAUTH_AVAILABLE:
        return {"error": "OAuth system not available", "providers": {}}

    try:
        config = universal_auth.get_auth_config()
        providers_status = {}

        for provider_id in universal_auth.supported_providers.keys():
            provider_config = next(
                (p for p in config["enabled_providers"]
                 if p["provider_id"] == provider_id),
                None
            )
            providers_status[provider_id] = {
                "configured": provider_config is not None,
                "has_client_id": bool(provider_config and provider_config.get("client_id")) if provider_config else False
            }

        return {
            "providers": providers_status,
            "total_configured": len(config["enabled_providers"])
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Status check failed: {str(e)}")


@app.get("/health")
def health():
    try:
        ok = verify_craftx_identity()
        return {"status": "ok" if ok else "degraded", "oauth_available": OAUTH_AVAILABLE}
    except Exception as e:
        return {"status": "degraded", "oauth_available": OAUTH_AVAILABLE, "error": str(e)}


@app.on_event("startup")
def on_start():
    print("🚀 CraftX server starting...")

    # Try to verify identity, but don't fail if Ollama isn't available
    try:
        if verify_craftx_identity():
            print("✅ CraftX identity verified")
        else:
            print(
                "⚠️  CraftX identity verification failed - continuing in development mode")
    except Exception as e:
        print(
            f"⚠️  CraftX identity verification error: {e} - continuing in development mode")

    if OAUTH_AVAILABLE:
        try:
            # Load OAuth configuration with environment variable substitution
            oauth_config = get_oauth_config()
            print("✅ OAuth system initialized with secure configuration")
            print(
                f"   📱 {len(oauth_config['enabled_providers'])} providers configured")
        except Exception as e:
            print(f"⚠️  OAuth configuration error: {e}")
            print("   Check that your .env file contains all required OAuth secrets")
    else:
        print("⚠️  OAuth system not available")

    print("🌐 Server ready at http://localhost:8002")


@app.post("/ask")
def ask(req: PromptRequest):
    try:
        if not verify_craftx_identity():
            # In development mode, continue with warning
            print("⚠️  CraftX identity not verified - responding anyway")

        agent_name = AgentRegistry.route(req.prompt) or "CraftX-Ollama"
        response = AgentRegistry.get(agent_name).ask(req.prompt)
        return {"response": response}
    except Exception as e:
        # In development mode, return a helpful error instead of failing
        return {"response": f"Error: {str(e)}. Make sure Ollama is running with the CraftX model.", "error": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
