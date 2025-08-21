# Netlify Environment Variables Setup Guide

Your OAuth authentication system is successfully deployed! Now you need to configure environment variables on Netlify to make the OAuth buttons work.

## Required Environment Variables

You need to set these environment variables in your Netlify dashboard:

### Google OAuth

- `GOOGLE_CLIENT_ID` - Your Google OAuth 2.0 Client ID
- `GOOGLE_CLIENT_SECRET` - Your Google OAuth 2.0 Client Secret

### GitHub OAuth

- `GITHUB_CLIENT_ID` - Your GitHub OAuth App Client ID
- `GITHUB_CLIENT_SECRET` - Your GitHub OAuth App Client Secret

### Microsoft OAuth

- `MICROSOFT_CLIENT_ID` - Your Azure AD App Client ID
- `MICROSOFT_CLIENT_SECRET` - Your Azure AD App Client Secret

### Apple OAuth (Optional)

- `APPLE_CLIENT_ID` - Your Apple OAuth Client ID

### ORCID OAuth (Optional)

- `ORCID_CLIENT_ID` - Your ORCID OAuth Client ID

### Okta OAuth (Optional)

- `OKTA_CLIENT_ID` - Your Okta OAuth Client ID
- `OKTA_DOMAIN` - Your Okta domain (e.g., <https://your-domain.okta.com>)

## How to Set Environment Variables on Netlify

### Method 1: Using Netlify CLI (Recommended)

```bash
# Set Google OAuth variables
netlify env:set GOOGLE_CLIENT_ID "your-google-client-id"
netlify env:set GOOGLE_CLIENT_SECRET "your-google-client-secret"

# Set GitHub OAuth variables
netlify env:set GITHUB_CLIENT_ID "your-github-client-id"
netlify env:set GITHUB_CLIENT_SECRET "your-github-client-secret"

# Set Microsoft OAuth variables
netlify env:set MICROSOFT_CLIENT_ID "your-microsoft-client-id"
netlify env:set MICROSOFT_CLIENT_SECRET "your-microsoft-client-secret"

# Optional: Set Apple OAuth variables
netlify env:set APPLE_CLIENT_ID "your-apple-client-id"

# Optional: Set ORCID OAuth variables
netlify env:set ORCID_CLIENT_ID "your-orcid-client-id"

# Optional: Set Okta OAuth variables
netlify env:set OKTA_CLIENT_ID "your-okta-client-id"
netlify env:set OKTA_DOMAIN "https://your-domain.okta.com"
```

### Method 2: Using Netlify Dashboard

1. Go to <https://app.netlify.com/sites/harmonious-naiad-3cd735/settings/deploys>
2. Scroll down to "Environment variables" section
3. Click "Add variable" for each required variable
4. Enter the variable name and value
5. Click "Save"

## OAuth Provider Redirect URIs

You also need to update your OAuth provider settings to use your Netlify domain:

### Google Cloud Console

- Authorized redirect URI: `https://harmonious-naiad-3cd735.netlify.app/callback/google`

### GitHub Developer Settings

- Authorization callback URL: `https://harmonious-naiad-3cd735.netlify.app/callback/github`

### Microsoft Azure AD

- Redirect URI: `https://harmonious-naiad-3cd735.netlify.app/callback/microsoft`

### Apple Developer Portal

- Return URL: `https://harmonious-naiad-3cd735.netlify.app/callback/apple`

### ORCID Developer Tools

- Redirect URI: `https://harmonious-naiad-3cd735.netlify.app/callback/orcid`

### Okta Developer Console

- Sign-in redirect URI: `https://harmonious-naiad-3cd735.netlify.app/callback/okta`

## Testing Your Setup

After setting environment variables and updating redirect URIs:

1. Redeploy your site to pick up the new environment variables:

   ```bash
   netlify deploy --prod
   ```

2. Visit your site: <https://harmonious-naiad-3cd735.netlify.app>

3. Click on each OAuth button to test the authentication flow

4. Check Netlify function logs for any errors:

   ```bash
   netlify logs --live
   ```

## Troubleshooting

### Common Issues

1. **"OAuth provider not configured"** - Environment variables not set correctly
2. **"Invalid redirect URI"** - OAuth provider redirect URI not updated
3. **CORS errors** - Already fixed in your netlify.toml configuration

### Debugging

- Use `netlify logs --live` to see real-time function logs
- Check browser developer tools console for JavaScript errors
- Verify environment variables are set: `netlify env:list`

## Next Steps

1. ✅ Deploy successful (DONE)
2. ⏳ Set environment variables (THIS STEP)
3. ⏳ Update OAuth provider redirect URIs
4. ⏳ Test OAuth authentication flow
5. ⏳ Test WebAuthn passkey authentication

Your OAuth system is ready to work once these environment variables are configured!
