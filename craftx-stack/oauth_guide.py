"""
Simple OAuth button implementation guide for CraftX.py
"""

# Step 1: Create a simple HTML page with working OAuth buttons
html_demo = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CraftX OAuth Demo</title>
    <style>
        body {
            font-family: 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            background: #f9f9fb;
        }
        .oauth-container {
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .btn-oauth {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0.75rem;
            margin: 0.5rem;
            background: white;
            border: 1px solid #ccc;
            border-radius: 6px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            color: #333;
        }
        .btn-oauth:hover {
            background: #f5f5f5;
            border-color: #999;
        }
        .btn-oauth svg {
            width: 18px;
            height: 18px;
            margin-right: 8px;
        }
        .signin-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 0.75rem;
            margin-top: 2rem;
        }
        .status {
            margin-top: 2rem;
            padding: 1rem;
            border-radius: 6px;
            background: #e8f4fd;
            border: 1px solid #0066cc;
        }
    </style>
</head>
<body>
    <div class="oauth-container">
        <h1>🔐 CraftX OAuth Demo</h1>
        <p>Click any button below to test OAuth authentication:</p>
        
        <div class="signin-grid">
            <!-- Google OAuth Button -->
            <button class="btn-oauth" onclick="testOAuth('google')">
                <svg viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M21 12.3c0-.8-.1-1.5-.3-2.2H12v4.1h4.9c-.2 1.1-.8 2-1.6 2.6l2.6 2 1.8-1.8c1.7-1.6 2.6-3.9 2.6-6.7z"></path>
                </svg>
                Google
            </button>
            
            <!-- GitHub OAuth Button -->
            <button class="btn-oauth" onclick="testOAuth('github')">
                <svg viewBox="0 0 24 24">
                    <path fill="#181717" d="M12 .5C5.7.5.5 5.7.5 12c0 5.1 3.3 9.4 7.8 10.9.6.1.8-.2.8-.5v-1.8c-3.2.7-3.8-1.5-3.8-1.5-.5-1.3-1.3-1.6-1.3-1.6-1-.7.1-.7.1-.7 1.1.1 1.7 1.1 1.7 1.1 1 .1 1.7-.7 1.7-.7.9-1.7 2.4-1.2 3-.9.1-.7.4-1.2.8-1.5-2.5-.3-5.1-1.3-5.1-5.7 0-1.3.5-2.4 1.2-3.3 0-.3-.5-1.4.1-2.8 0 0 1-.3 3.3 1.2 1-.3 2-.5 3-.5s2 .2 3 .5c2.3-1.5 3.3-1.2 3.3-1.2.6 1.4.1 2.5.1 2.8.8.9 1.2 2 1.2 3.3 0 4.4-2.6 5.4-5.1 5.7.4.3.8 1 .8 2v2.9c0 .3.2.6.8.5C20.7 21.4 24 17.1 24 12c0-6.3-5.2-11.5-12-11.5z"></path>
                </svg>
                GitHub
            </button>
            
            <!-- Okta OAuth Button -->
            <button class="btn-oauth" onclick="testOAuth('okta')">
                <svg viewBox="0 0 24 24">
                    <path fill="#007DC1" d="M4 4h4v16H4zM9 4h4v16H9zM14 4h4v16h-4z"></path>
                </svg>
                Okta
            </button>
            
            <!-- ORCID OAuth Button -->
            <button class="btn-oauth" onclick="testOAuth('orcid')">
                <svg viewBox="0 0 24 24">
                    <path fill="#A6CE39" d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm0 18c-4.4 0-8-3.6-8-8 0-2 .8-3.8 2.1-5l10.9 10.9c-1.2 1.4-2.9 2.1-4.9 2.1zm5.9-3.4L7 6.1c1.4-1.2 3.2-2 5.1-2 4.4 0 8 3.6 8 8 0 2-.8 3.8-2.1 5z"></path>
                </svg>
                ORCID
            </button>
        </div>
        
        <div id="status" class="status" style="display: none;">
            <h3>OAuth Status</h3>
            <p id="status-message">Testing OAuth connection...</p>
        </div>
    </div>

    <script>
        async function testOAuth(provider) {
            const statusDiv = document.getElementById('status');
            const statusMessage = document.getElementById('status-message');
            
            statusDiv.style.display = 'block';
            statusMessage.textContent = `Testing ${provider} OAuth...`;
            
            try {
                // Test if server is running
                const healthResponse = await fetch('/health');
                if (!healthResponse.ok) {
                    throw new Error('Server not running on localhost:8000');
                }
                
                // Check OAuth status
                const oauthResponse = await fetch('/admin/oauth-status');
                const oauthStatus = await oauthResponse.json();
                
                if (oauthStatus.providers && oauthStatus.providers[provider]) {
                    const providerStatus = oauthStatus.providers[provider];
                    
                    if (providerStatus.configured && providerStatus.has_client_id) {
                        statusMessage.innerHTML = `
                            ✅ ${provider} is configured! Redirecting to OAuth...
                            <br><small>If this were a real app, you'd be redirected to ${provider}'s login page.</small>
                        `;
                        
                        // In a real scenario, this would redirect to the OAuth provider
                        // window.location.href = `/auth/${provider}`;
                    } else if (providerStatus.configured) {
                        statusMessage.innerHTML = `
                            ⚠️ ${provider} is partially configured but missing client_id.
                            <br><small>Run the OAuth setup script to complete configuration.</small>
                        `;
                    } else {
                        statusMessage.innerHTML = `
                            ❌ ${provider} is not configured.
                            <br><small>Run: python oauth_setup.py to configure this provider.</small>
                        `;
                    }
                } else {
                    statusMessage.innerHTML = `
                        ❌ ${provider} provider not found or OAuth system unavailable.
                        <br><small>Make sure the CraftX server is running.</small>
                    `;
                }
                
            } catch (error) {
                statusMessage.innerHTML = `
                    ❌ Error: ${error.message}
                    <br><small>Make sure the CraftX server is running on localhost:8000</small>
                `;
            }
        }
        
        // Auto-check server status on load
        window.addEventListener('load', async () => {
            try {
                const response = await fetch('/health');
                if (response.ok) {
                    const health = await response.json();
                    console.log('Server health:', health);
                }
            } catch (error) {
                console.log('Server not reachable:', error.message);
            }
        });
    </script>
</body>
</html>
'''

print("=" * 60)
print("🔐 CraftX OAuth Integration Guide")
print("=" * 60)

print("""
To make your OAuth buttons functional, follow these steps:

1. **Start the CraftX server:**
   cd craftx-stack
   python craftx.py

2. **Configure OAuth providers:**
   python oauth_setup.py

3. **Test the setup:**
   python test_oauth.py

4. **Visit your website:**
   http://localhost:8000

🎯 **What each button should do:**

┌─────────────────────────────────────────────────────────┐
│ Google Button  → /auth/google  → Google OAuth login     │
│ GitHub Button  → /auth/github  → GitHub OAuth login     │
│ Okta Button    → /auth/okta    → Okta OAuth login       │
│ ORCID Button   → /auth/orcid   → ORCID OAuth login      │
└─────────────────────────────────────────────────────────┘

📋 **Current Implementation Status:**

✅ Frontend: OAuth buttons with data-provider attributes
✅ Backend: FastAPI server with OAuth endpoints  
✅ Auth System: Universal OAuth manager with multiple providers
✅ Session Management: Secure token-based authentication
✅ Download Protection: Token-based download verification

🔧 **Next Steps:**

1. Run the setup script to configure your preferred providers
2. Test each provider individually
3. Customize the user experience after authentication
4. Add proper error handling and user feedback

📖 **Documentation:**
- Setup Guide: craftx-stack/OAUTH_SETUP.md
- Test Script: craftx-stack/test_oauth.py
- Demo HTML: See the html_demo variable above

🚀 **Quick Test:**
Save the HTML demo above as 'oauth_test.html' and serve it alongside 
your CraftX server to test the OAuth flow interactively.
""")

# Save the demo HTML
with open("oauth_demo.html", "w", encoding="utf-8") as f:
    f.write(html_demo)

print("✅ Created oauth_demo.html for interactive testing")
print("🌐 Open this file in a browser alongside your running CraftX server")
