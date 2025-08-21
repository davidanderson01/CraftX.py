# Auth0 Setup for GitHub Pages OAuth

## Step 1: Create Auth0 Account

1. Go to [auth0.com](https://auth0.com) and sign up for free
2. Create a new application (Single Page Application)
3. Note your **Domain** and **Client ID**

## Step 2: Configure OAuth Providers in Auth0

1. Go to **Authentication** > **Social**
2. Enable the providers you want:
   - Google OAuth 2.0
   - GitHub
   - Microsoft
   - Apple (requires Apple Developer account)

## Step 3: Configure Application Settings

In your Auth0 application settings:

**Allowed Callback URLs:**

```text
https://yourusername.github.io/CraftX.py,
https://yourusername.github.io/CraftX.py/,
http://localhost:3000
```

**Allowed Logout URLs:**

```text
https://yourusername.github.io/CraftX.py,
https://yourusername.github.io/CraftX.py/
```

**Allowed Web Origins:**

```text
https://yourusername.github.io,
http://localhost:3000
```

## Step 4: Update Your index.html

Replace the OAuth button functions with Auth0 integration:

```javascript
// Replace the current OAuth functions with Auth0
let auth0Client = null;

// Initialize Auth0
window.onload = async () => {
    auth0Client = await createAuth0Client({
        domain: 'YOUR_AUTH0_DOMAIN.auth0.com',
        clientId: 'YOUR_AUTH0_CLIENT_ID',
        authorizationParams: {
            redirect_uri: window.location.origin
        }
    });
    
    // Check if user is authenticated
    const isAuthenticated = await auth0Client.isAuthenticated();
    if (isAuthenticated) {
        updateUIForAuthenticatedUser();
    }
};

async function authenticateWith(provider) {
    await auth0Client.loginWithRedirect({
        authorizationParams: {
            connection: getAuth0Connection(provider)
        }
    });
}

function getAuth0Connection(provider) {
    const connections = {
        google: 'google-oauth2',
        github: 'github',
        microsoft: 'windowslive',
        apple: 'apple'
    };
    return connections[provider];
}
```

## Step 5: Benefits of This Approach

✅ **No server required** - works perfectly with GitHub Pages
✅ **Secure** - Auth0 handles all the OAuth complexity
✅ **Free tier** - up to 7,000 monthly active users
✅ **Multiple providers** - Google, GitHub, Microsoft, Apple, etc.
✅ **User management** - built-in user database
✅ **Analytics** - user login analytics

## Alternative: Direct OAuth (Limited)

If you prefer not to use Auth0, you can use client-side OAuth for some providers (GitHub works well):

```javascript
function authenticateGitHub() {
    const clientId = 'your-github-client-id'; // Public client ID
    const redirectUri = window.location.origin;
    const scope = 'user:email';
    
    window.location.href = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}`;
}
```

**Note**: This approach has limitations - you can't securely exchange the authorization code for tokens on the client side.

## Recommendation

Use **Auth0** - it's specifically designed for this use case and works perfectly with GitHub Pages!
