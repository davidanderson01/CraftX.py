# 🎓 ORCID OAuth Setup Guide

## The Problem

ORCID has strict security requirements and **only accepts HTTPS redirect URIs** in production. Your current setup using `http://localhost:8000` won't work with ORCID.

## ✅ Solution Options

### Option 1: Production Setup (Recommended)

For your live website at <https://craftx.elevatecraft.org>:

**ORCID Application Settings:**

- **Application name:** `CraftX.py`
- **Application URL:** `https://craftx.elevatecraft.org`
- **Application description:** `CraftX.py is a modular, Python-native AI framework designed for building intelligent applications with ease. It provides a clean, extensible architecture for integrating multiple AI models, managing conversations, and extending functionality through plugins.`
- **Redirect URI:** `https://craftx.elevatecraft.org/auth/callback/orcid`

### Option 2: Development Testing

For local development, you have two choices:

#### A) Use ORCID Sandbox

- Go to: <https://sandbox.orcid.org/developer-tools>
- Create a sandbox application
- Use sandbox credentials for testing
- Note: Sandbox uses different API endpoints

#### B) Skip ORCID for Local Development

- Configure other providers (Google, GitHub, Okta) for local testing
- Deploy ORCID only to production environment

### Option 3: HTTPS Tunnel for Local Development

Use a tool like ngrok to create HTTPS tunnel:

```bash
# Install ngrok
# Download from: https://ngrok.com/

# Create HTTPS tunnel to your local server
ngrok http 8000

# Use the HTTPS URL for ORCID redirect:
# https://abc123.ngrok.io/auth/callback/orcid
```

## 🔧 Recommended Setup Steps

### For Production (craftx.elevatecraft.org)

1. **Update ORCID Application:**
   - Application URL: `https://craftx.elevatecraft.org`
   - Redirect URI: `https://craftx.elevatecraft.org/auth/callback/orcid`

2. **Deploy Your Server:**
   - Ensure your FastAPI server is deployed to craftx.elevatecraft.org
   - Verify HTTPS is working
   - Test the redirect endpoint

3. **Configure OAuth:**
   - Use the production ORCID credentials
   - Update your auth_config.json with production settings

### For Local Development

1. **Skip ORCID temporarily:**
   - Test with Google, GitHub, Microsoft instead
   - These providers allow HTTP localhost for development

2. **OR use ORCID Sandbox:**
   - Register at: <https://sandbox.orcid.org/developer-tools>
   - Use sandbox API endpoints
   - Note: Different base URL for sandbox

## 📝 Current Settings You Should Use

**In your ORCID application form:**

```
Application name: CraftX.py
Application URL: https://craftx.elevatecraft.org
Application description: CraftX.py is a modular, Python-native AI framework designed for building intelligent applications with ease. It provides a clean, extensible architecture for integrating multiple AI models, managing conversations, and extending functionality through plugins.
Redirect URIs: https://craftx.elevatecraft.org/auth/callback/orcid
```

## 🚨 Important Notes

1. **HTTPS Only:** ORCID requires HTTPS in production - no exceptions
2. **Exact Match:** Redirect URIs must match exactly (including trailing slashes)
3. **Domain Verification:** ORCID verifies domain ownership
4. **Non-Commercial:** Ensure you comply with ORCID's non-commercial terms

## 🧪 Testing Your Setup

Once configured, test with:

- Production: <https://craftx.elevatecraft.org>
- Click ORCID OAuth button
- Should redirect to ORCID login
- After login, should return to your site

## 🔍 Alternative Providers for Local Development

While setting up ORCID for production, you can test locally with:

- ✅ **Google:** Allows localhost for development
- ✅ **GitHub:** Allows localhost for development  
- ✅ **Microsoft:** Allows localhost for development
- ✅ **Auth0:** Allows localhost for development

These providers are more developer-friendly for local testing!
