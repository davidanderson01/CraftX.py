# OAuth Configuration for CraftX.py on GitHub Pages

## Provider Details

### GitHub OAuth

- **Client ID:** `Ov23liXXXXXXXXXXXXX` (Replace with your GitHub OAuth App Client ID)
- **Client Secret:** `ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` (Replace with your GitHub OAuth App Client Secret)
- **Redirect URI:** `https://davidanderson01.github.io/CraftX.py/`
- **Scope:** `user:email`

### Google OAuth

- **Client ID:** `123456789012-abcdefghijklmnopqrstuvwxyz123456.apps.googleusercontent.com`
- **Client Secret:** `GOCSPX-abcdefghijklmnopqrstuvwxyz123456`
- **Redirect URI:** `https://davidanderson01.github.io/CraftX.py/`
- **Scope:** `openid email profile`

### Apple OAuth (Sign In with Apple)

- **Service ID:** `com.yourcompany.yourapp` (Replace with your Apple Service ID)
- **Team ID:** `XXXXXXXXXX` (Replace with your Apple Developer Team ID)
- **Key ID:** `XXXXXXXXXX` (Replace with your Apple Key ID)
- **Private Key File:** `AuthKey_XXXXXXXXXX.p8` (Replace with your Apple Private Key file)
- **Redirect URI:** `https://davidanderson01.github.io/CraftX.py/apple-callback.html`

### OKTA OAuth

- **Client ID:** `0oaXXXXXXXXXXXXXXXXX` (Replace with your OKTA Client ID)
- **Client Secret:** `XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` (Replace with your OKTA Client Secret)
- **Domain:** `your-domain.okta.com` (Replace with your OKTA domain)
- **Redirect URI:** `https://davidanderson01.github.io/CraftX.py/`
- **Scope:** `openid email profile`

### ORCID OAuth

- **Client ID:** `APP-XXXXXXXXXXXXXXXX` (Replace with your ORCID Client ID)
- **Client Secret:** `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` (Replace with your ORCID Client Secret)
- **Redirect URI:** `https://davidanderson01.github.io/CraftX.py/`
- **Scope:** `/authenticate`

### WebAuthn/Passkey Configuration

- **Raw ID:** `XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` (Replace with your WebAuthn credential Raw ID)
- **Public Key Algorithm:** `ECDSA_w_SHA256`
- **Curve:** `P-256`

## GitHub Pages Setup

### Required Files Created

1. `index.html` - Updated with GitHub Pages OAuth
2. `apple-signin.html` - Apple Sign In page
3. `apple-callback.html` - Apple OAuth callback handler

### How It Works

1. **Client-Side OAuth Flow:** All OAuth happens in the browser
2. **No Server Required:** Perfect for GitHub Pages static hosting
3. **Secure State Management:** CSRF protection with state parameters
4. **Multi-Provider Support:** GitHub, Google, Apple, OKTA, ORCID

### Provider Configuration Notes

#### GitHub

- ✅ Ready to use with client-side flow
- Update redirect URI in GitHub App settings to your GitHub Pages URL

#### Google

- ✅ Ready to use with client-side flow  
- Update redirect URI in Google Cloud Console

#### Apple

- ⚠️ Requires additional setup in Apple Developer Console
- Update Service ID configuration with GitHub Pages URL
- Verify domain in Apple Developer Console

#### OKTA

- ✅ Ready to use
- Update redirect URI in OKTA application settings

#### ORCID

- ✅ Ready to use
- Update redirect URI in ORCID application settings

## Next Steps

1. **Update Redirect URIs:** In each provider's console, update redirect URIs to:
   - `https://davidanderson01.github.io/CraftX.py/` (for most providers)
   - `https://davidanderson01.github.io/CraftX.py/apple-callback.html` (for Apple)

2. **Test Each Provider:** Use the OAuth buttons to test each authentication flow

3. **Update Apple Domain:** Verify `davidanderson01.github.io` in Apple Developer Console

4. **Deploy:** Commit and push all changes to GitHub

## Security Notes

- Client IDs are public and safe to include in client-side code
- Client secrets are NOT used in client-side flows (more secure)
- State parameters prevent CSRF attacks
- All authentication happens on provider's secure servers
