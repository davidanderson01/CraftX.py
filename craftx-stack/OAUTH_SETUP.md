# CraftX OAuth Authentication Setup

This guide helps you configure OAuth authentication for your CraftX deployment, making the OAuth buttons on your website functional.

## Quick Start

1. **Setup analytics (optional but recommended):**

   ```bash
   python setup_analytics.py
   ```

2. **Run the OAuth setup script:**

   ```bash
   cd craftx-stack
   python oauth_setup.py
   ```

3. **Start the CraftX server:**

   ```bash
   python craftx.py
   ```

4. **Visit your website:**

   ```text
   http://localhost:8000
   ```

5. **View analytics dashboard:**

   ```text
   http://localhost:8000/admin/analytics
   ```

## Supported OAuth Providers

- **Google** - Google Cloud OAuth
- **GitHub** - GitHub OAuth Apps
- **Microsoft** - Azure AD/Microsoft Account
- **Okta** - Okta Identity Platform
- **ORCID** - Academic/Research Authentication
- **Apple** - Apple ID Sign-In
- **Auth0** - Auth0 Identity Platform
- **Discord** - Discord OAuth
- **LinkedIn** - LinkedIn OAuth
- **Twitter/X** - Twitter OAuth

## Provider Setup Instructions

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing project
3. Enable Google+ API
4. Navigate to **Credentials** → **Create credentials** → **OAuth 2.0 Client IDs**
5. Choose **Web application**
6. Add authorized redirect URI: `http://localhost:8000/auth/callback/google`
7. Copy the **Client ID** and **Client Secret**

### GitHub OAuth Setup

1. Go to GitHub **Settings** → **Developer settings** → **OAuth Apps**
2. Click **New OAuth App**
3. Set **Authorization callback URL**: `http://localhost:8000/auth/callback/github`
4. Copy the **Client ID** and generate a **Client Secret**

### Microsoft OAuth Setup

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Click **New registration**
4. Set redirect URI: `http://localhost:8000/auth/callback/microsoft`
5. Copy **Application (client) ID** and create a **client secret**

### Okta OAuth Setup

1. Go to [Okta Developer Console](https://dev.okta.com/)
2. Create a new app integration
3. Choose **OIDC - OpenID Connect** → **Web Application**
4. Set Sign-in redirect URIs: `http://localhost:8000/auth/callback/okta`
5. Copy **Client ID** and **Client Secret**
6. Note your Okta domain (e.g., `dev-123456.okta.com`)

### ORCID OAuth Setup

1. Go to [ORCID Developer Tools](https://orcid.org/developer-tools)
2. Register for a developer account
3. Create a new application
4. Set redirect URI: `http://localhost:8000/auth/callback/orcid`
5. Copy **Client ID** and **Client Secret**

## Manual Configuration

If you prefer to configure providers manually, you can use the admin API:

```bash
curl -X POST "http://localhost:8000/admin/configure-oauth" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "google",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret"
  }'
```

For domain-based providers (Okta, Auth0):

```bash
curl -X POST "http://localhost:8000/admin/configure-oauth" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "okta",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "domain": "your-domain.okta.com"
  }'
```

## Check Configuration Status

View the current OAuth configuration:

```bash
curl http://localhost:8000/admin/oauth-status
```

## Testing OAuth Flow

1. Start the server: `python craftx.py`
2. Visit: `http://localhost:8000`
3. Click any configured OAuth provider button
4. Complete the authentication flow
5. You should be redirected back with a download token

## How It Works

1. **User clicks OAuth button** → Redirects to `/auth/{provider}`
2. **Server generates OAuth URL** → Redirects user to provider's auth page
3. **User authenticates** → Provider redirects to `/auth/callback/{provider}`
4. **Server processes callback** → Creates user session and download token
5. **User gets download access** → Can download CraftX with authenticated token

## File Structure

```text
craftx-stack/
├── craftx.py              # Main FastAPI server with OAuth endpoints
├── oauth_setup.py         # Interactive OAuth configuration script
├── setup_analytics.py     # Analytics system setup script
├── user_analytics.py      # User tracking and analytics system
├── analytics_dashboard.py # Web dashboard for analytics
├── oauth_states/          # Temporary OAuth state storage
├── download_tokens/       # Download token storage
├── auth_config.json       # OAuth provider configuration
└── user_analytics.db      # SQLite database for user analytics
```

## Analytics Features

The CraftX analytics system automatically tracks:

- **👥 User Registration**: New user sign-ups by provider
- **🔐 Authentication Events**: Login attempts, successes, and failures
- **📊 User Demographics**: Geographic distribution, device types, browsers
- **📈 Download Tracking**: Who downloads CraftX and when
- **⏱️ Session Management**: Active users and session duration
- **📱 Device Analytics**: Mobile vs desktop usage patterns
- **🌍 Geographic Data**: Country/city distribution (with GeoIP)

### Analytics Dashboard

Visit `http://localhost:8000/admin/analytics` to view:

- Real-time user statistics
- Interactive charts and graphs
- Recent user activity table
- Export functionality (JSON/CSV)
- Provider and device breakdowns

## Security Notes

- OAuth states are stored temporarily and cleaned up after use
- Download tokens expire after 1 hour
- Session data is stored securely with timestamps
- HTTPS is recommended for production deployments
- Client secrets should be kept secure and not committed to version control

## Troubleshooting

### OAuth System Not Available

```text
⚠️ OAuth system not available. OAuth endpoints will be disabled.
```

**Solution**: Make sure you're running from the `craftx-stack` directory and the auth module is accessible.

### Invalid Redirect URI

```text
Error: redirect_uri_mismatch
```

**Solution**: Ensure the redirect URI in your OAuth provider settings exactly matches:
`http://localhost:8000/auth/callback/{provider}`

### Provider Not Configured

```text
Provider google not configured or missing client_id
```

**Solution**: Run `python oauth_setup.py` to configure the provider credentials.

## Production Deployment

For production deployments:

1. **Use HTTPS**: Update redirect URIs to use `https://`
2. **Secure storage**: Use proper database for sessions and tokens
3. **Environment variables**: Store client secrets in environment variables
4. **Rate limiting**: Implement rate limiting for OAuth endpoints
5. **Monitoring**: Add logging and monitoring for OAuth flows

## Support

- 📖 [CraftX Documentation](https://davidanderson01.github.io/CraftX.py/)
- 🐛 [Report Issues](https://github.com/davidanderson01/CraftX.py/issues)
- 💬 [Community Support](https://github.com/davidanderson01/CraftX.py/discussions)
