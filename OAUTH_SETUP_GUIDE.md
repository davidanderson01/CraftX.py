# OAuth Setup Guide for Netlify

You're very close! Here's what you need to complete the OAuth setup:

## ✅ What's Already Done

1. **Netlify Functions**: Complete OAuth handler at `netlify/functions/oauth-handler.js`
2. **WebAuthn Support**: Passkey authentication with `netlify/functions/webauthn-handler.js`
3. **Frontend Integration**: Updated `index.html` with OAuth buttons + Passkey authentication
4. **Configuration Files**: `package.json`, `netlify.toml` are set up
5. **Deployment**: Site deployed to `harmonious-naiad-3cd735.netlify.app`

## 🔧 What You Need to Configure

### 1. Environment Variables on Netlify

Go to your Netlify dashboard:

1. Log into [netlify.com](https://netlify.com)
2. Go to your site: **harmonious-naiad-3cd735**
3. Navigate to **Site settings** → **Environment variables**
4. Add these variables:

#### Required for Google OAuth

```env
GOOGLE_CLIENT_ID = your_google_client_id
GOOGLE_CLIENT_SECRET = your_google_client_secret
```

#### Required for GitHub OAuth

```env
GITHUB_CLIENT_ID = your_github_client_id
GITHUB_CLIENT_SECRET = your_github_client_secret
```

#### Required for Microsoft OAuth

```env
MICROSOFT_CLIENT_ID = your_microsoft_client_id
MICROSOFT_CLIENT_SECRET = your_microsoft_client_secret
```

### 2. Update OAuth Provider Redirect URIs

For each OAuth provider you want to use, update the redirect URI to:

**New Redirect URI**: `https://harmonious-naiad-3cd735.netlify.app/.netlify/functions/oauth-handler/{provider}`

#### Google OAuth Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services** → **Credentials**
3. Find your OAuth 2.0 Client ID
4. Add redirect URI: `https://harmonious-naiad-3cd735.netlify.app/.netlify/functions/oauth-handler/google`

#### GitHub OAuth Settings

1. Go to GitHub **Settings** → **Developer settings** → **OAuth Apps**
2. Find your OAuth app
3. Update **Authorization callback URL**: `https://harmonious-naiad-3cd735.netlify.app/.netlify/functions/oauth-handler/github`

#### Microsoft Azure AD

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** → **App registrations**
3. Find your app registration
4. Go to **Authentication** → **Redirect URIs**
5. Add: `https://harmonious-naiad-3cd735.netlify.app/.netlify/functions/oauth-handler/microsoft`

## 🚀 Deployment Steps

1. **Push your changes to GitHub** (the updated files)
2. **Netlify will auto-deploy** the new serverless function
3. **Add environment variables** in Netlify dashboard
4. **Update OAuth provider redirect URIs** as shown above
5. **Test the OAuth buttons** on your live site

## 🧪 Testing

Once configured, visit `https://harmonious-naiad-3cd735.netlify.app` and:

### OAuth Testing

1. Click any OAuth button (Google, GitHub, Microsoft)
2. You should be redirected to the provider's login page
3. After authentication, you'll be redirected back with a success message
4. The download link should appear

### WebAuthn/Passkey Testing

1. Click the "Sign in with Passkey" button
2. Your browser will prompt for biometric authentication (fingerprint, face, or security key)
3. If you have the configured credential (`49cdd33f...`), authentication should succeed
4. You'll see a success message and download access will be enabled

**Note**: The current WebAuthn setup recognizes a specific test credential. For production, you'd implement full credential registration.

## 🔍 Troubleshooting

If OAuth isn't working:

1. **Check Netlify Functions logs**: Site settings → Functions → View logs
2. **Verify environment variables**: Make sure all required variables are set
3. **Check redirect URIs**: Ensure they match exactly in your OAuth provider settings
4. **Clear browser cache**: Sometimes old redirects get cached

## 📋 Current Status

- ✅ Serverless function created
- ✅ Frontend updated  
- ✅ Configuration files ready
- ✅ Deployed to Netlify
- ⏳ **Need**: Environment variables
- ⏳ **Need**: OAuth provider redirect URI updates

You're just two steps away from having fully functional OAuth!
