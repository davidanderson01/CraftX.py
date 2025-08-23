# Callback/Webhook helper (no new accounts, free)

This folder contains a tiny Python stdlib server you can run locally and (optionally) expose over the internet via a free, no-signup tunnel.

What you get:

- `/oauth/callback` (GET) for OAuth/OIDC redirects (logs query like `code`, `state`, `id_token`).
- `/apple/notifications` (POST) for Apple S2S notifications (logs body, returns 200).
- `/healthz` (GET) liveness.

## Run locally

```powershell
# From repo root
python callbacks/server.py --port 8787
```

Local callback URL examples:

- <http://127.0.0.1:8787/oauth/callback>
- <http://127.0.0.1:8787/apple/notifications>

## Expose publicly without creating an account

Pick one of these free options; neither requires sign-up:

1) Cloudflared quick tunnel

- Install (one-liner): <https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/>
- Run:

```powershell
cloudflared tunnel --url http://127.0.0.1:8787
```

- It prints a `https://*.trycloudflare.com` URL. Use that as your public callback base.

2) LocalXpose (anon quick URL)

- Download: <https://localxpose.io/downloads>
- Run:

```powershell
lxh http 8787
```

- It prints a temporary public URL.

Both are free for ad-hoc testing. For production, use Okta-hosted callback or your own domain.

## Configure providers for testing

- GitHub/Apple/ORCID: set callback/redirect URL to `<public-url>/oauth/callback`.
- If testing Apple S2S, set webhook to `<public-url>/apple/notifications`.

## Notes

- This server stores nothing. It only logs to the console.
- Keep the tunnel window open during testing.
- Remove the public tunnel when done.
