@echo off
echo ========================================
echo CraftX OAuth Setup - Step by Step Guide
echo ========================================
echo.

echo STEP 1: Starting CraftX Server
echo ===============================
echo.
echo Navigate to the craftx-stack directory and start the server:
echo.
echo   cd craftx-stack
echo   python craftx.py
echo.
echo You should see output like:
echo   "🚀 CraftX server starting..."
echo   "✅ OAuth system initialized"
echo   "🌐 Server ready at http://localhost:8002"
echo.
echo Leave this terminal open and running!
echo.

echo STEP 2: Configure OAuth Providers
echo ==================================
echo.
echo In a NEW terminal/command prompt, run:
echo.
echo   cd craftx-stack
echo   python oauth_setup.py
echo.
echo Follow the interactive prompts to configure providers like:
echo.
echo 🔍 Google OAuth:
echo   - Go to: https://console.cloud.google.com/
echo   - Create OAuth 2.0 Client ID
echo   - Set redirect URI: https://craftx.elevatecraft.org/auth/callback/google
echo   - Copy Client ID and Secret
echo.
echo 🐙 GitHub OAuth:
echo   - Go to: https://github.com/settings/developers
echo   - Create New OAuth App
echo   - Set callback URL: https://craftx.elevatecraft.org/auth/callback/github
echo   - Copy Client ID and Secret
echo.
echo 🏢 Okta OAuth:
echo   - Go to: https://dev.okta.com/
echo   - Create app integration (Web Application)
echo   - Set redirect URI: https://craftx.elevatecraft.org/auth/callback/okta
echo   - Copy Client ID and Secret + Domain
echo.
echo 🎓 ORCID OAuth:
echo   - Go to: https://orcid.org/developer-tools
echo   - Register application
echo   - Application URL: https://craftx.elevatecraft.org
echo   - For LOCAL TESTING: Use sandbox environment
echo   - PRODUCTION redirect URI: https://craftx.elevatecraft.org/auth/callback/orcid
echo   - SANDBOX redirect URI: https://sandbox.orcid.org (for testing)
echo   - NOTE: ORCID requires HTTPS in production, no HTTP allowed!
echo   - Copy Client ID and Secret
echo.

echo STEP 3: Test Your Setup
echo ========================
echo.
echo Run the test script:
echo.
echo   python test_oauth.py
echo.
echo This will verify:
echo   ✅ Server is running
echo   ✅ OAuth system is available
echo   ✅ Providers are configured
echo   ✅ Endpoints are working
echo.

echo STEP 4: Test Your Website
echo ==========================
echo.
echo Visit: http://localhost:8002
echo.
echo Click any configured OAuth button to test the flow:
echo   - Google → http://localhost:8002/auth/google (redirects to https://craftx.elevatecraft.org)
echo   - GitHub → http://localhost:8002/auth/github (redirects to https://craftx.elevatecraft.org)
echo   - Okta → http://localhost:8002/auth/okta (redirects to https://craftx.elevatecraft.org)
echo   - ORCID → http://localhost:8002/auth/orcid (redirects to https://craftx.elevatecraft.org)
echo.

echo ========================================
echo QUICK START (Copy-Paste Commands)
echo ========================================
echo.
echo Terminal 1 (Server):
echo   cd craftx-stack
echo   python craftx.py
echo.
echo Terminal 2 (Setup):
echo   cd craftx-stack
echo   python oauth_setup.py
echo.
echo Terminal 3 (Test):
echo   cd craftx-stack
echo   python test_oauth.py
echo.

echo ========================================
echo TROUBLESHOOTING
echo ========================================
echo.
echo If you see errors:
echo.
echo ❌ "OAuth system not available"
echo   → Make sure you're in the craftx-stack directory
echo   → Check that craftxpy.utils.auth module is accessible
echo.
echo ❌ "Server not running"
echo   → Make sure python craftx.py is running in Terminal 1
echo   → Check that port 8002 is not blocked
echo.
echo ❌ "Provider not configured"
echo   → Run python oauth_setup.py
echo   → Follow the setup instructions for each provider
echo.
echo ❌ "Redirect URI mismatch"
echo   → Make sure redirect URIs in OAuth providers exactly match:
echo     ALL PROVIDERS: https://craftx.elevatecraft.org/auth/callback/{provider}
echo   → Google: https://craftx.elevatecraft.org/auth/callback/google
echo   → GitHub: https://craftx.elevatecraft.org/auth/callback/github
echo   → Okta: https://craftx.elevatecraft.org/auth/callback/okta
echo   → ORCID: https://craftx.elevatecraft.org/auth/callback/orcid
echo   → All providers now use HTTPS production URLs for security
echo.

echo ========================================
echo WHAT HAPPENS WHEN IT WORKS
echo ========================================
echo.
echo 1. User clicks OAuth button (e.g., "Google")
echo 2. Browser redirects to: /auth/google
echo 3. Server redirects to: https://accounts.google.com/oauth/authorize...
echo 4. User logs in with Google
echo 5. Google redirects back to: /auth/callback/google
echo 6. Server creates session and download token
echo 7. User redirected back to your site with access
echo 8. Download is now enabled for that user
echo.

echo ========================================
echo YOUR OAUTH BUTTONS ARE NOW FUNCTIONAL!
echo ========================================
echo.
pause
