# 🚀 OAuth Deployment Solutions for CraftX

## 🎯 **Current Problem**

Your website is hosted as a **static site on GitHub Pages**, but OAuth authentication requires **server-side endpoints** to handle the authentication flow. This causes 404 errors when users click OAuth buttons.

## ✅ **Solution Options**

### **🔥 Option 1: Netlify Functions (Recommended)**

Deploy your site to **Netlify** with serverless functions to handle OAuth:

#### **Netlify Setup Steps:**

1. **Create Netlify Account**

   ```bash
   # Install Netlify CLI
   npm install -g netlify-cli
   
   # Login to Netlify
   netlify login
   ```

1. **Configure OAuth Apps**
   - **Google**: [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - **GitHub**: [GitHub Developer Settings](https://github.com/settings/developers)
   - **Microsoft**: [Azure App Registrations](https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/RegisteredApps)
   - **Add redirect URI**: `https://your-site.netlify.app/.netlify/functions/oauth-handler/callback/{provider}`

1. **Deploy to Netlify**

   ```bash
   # Initialize Netlify project
   netlify init
   
   # Set environment variables
   netlify env:set GOOGLE_CLIENT_ID "your_google_client_id"
   netlify env:set GOOGLE_CLIENT_SECRET "your_google_client_secret"
   netlify env:set GITHUB_CLIENT_ID "your_github_client_id"
   netlify env:set GITHUB_CLIENT_SECRET "your_github_client_secret"
   # ... add other providers
   
   # Deploy
   netlify deploy --prod
   ```

1. **Point Custom Domain**
   - In Netlify dashboard: Site settings → Domain management
   - Add custom domain: `craftx.elevatecraft.org`
   - Update DNS to point to Netlify

#### **✅ Benefits:**

- ✅ Works with static site hosting
- ✅ Serverless (auto-scaling)
- ✅ Free tier available
- ✅ Easy deployment
- ✅ Built-in SSL/CDN

---

### **⚡ Option 2: Vercel Serverless Functions**

Similar to Netlify but using Vercel:

#### **Vercel Setup Steps:**

1. **Install Vercel CLI**

   ```bash
   npm install -g vercel
   vercel login
   ```

1. **Create Vercel Functions**

```javascript
// api/auth/[provider].js
export default async function handler(req, res) {
  const { provider } = req.query;
  // OAuth init logic
}

// api/callback/[provider].js
export default async function handler(req, res) {
  const { provider } = req.query;
  // OAuth callback logic
}
```

1. **Deploy**

   ```bash
   vercel --prod
   ```

---

### **🔧 Option 3: GitHub Pages + External Auth Service**

Keep GitHub Pages but use a third-party auth service:

#### **Services to Consider:**

- **Auth0** (easiest setup)
- **Firebase Auth**
- **AWS Cognito**
- **Supabase Auth**

#### **Example with Auth0:**

```html
<!-- Add Auth0 SDK -->
<script src="https://cdn.auth0.com/js/auth0-spa-js/2.0/auth0-spa-js.production.js"></script>

<script>
let auth0Client;

window.onload = async () => {
  auth0Client = await auth0.createAuth0Client({
    domain: 'your-domain.auth0.com',
    clientId: 'your-client-id',
    authorizationParams: {
      redirect_uri: window.location.origin
    }
  });
  
  // Handle OAuth buttons
  document.querySelectorAll('.btn-oauth').forEach(btn => {
    btn.addEventListener('click', async () => {
      const provider = btn.dataset.provider;
      await auth0Client.loginWithRedirect({
        authorizationParams: {
          connection: provider // 'google-oauth2', 'github', etc.
        }
      });
    });
  });
};
</script>
```

---

### **🏗️ Option 4: Hybrid Setup (GitHub Pages + Separate API)**

Keep your main site on GitHub Pages but deploy the OAuth endpoints separately:

#### **Structure:**

- **Main Site**: `craftx.elevatecraft.org` (GitHub Pages)
- **API Server**: `api.craftx.elevatecraft.org` (Railway/Render/Heroku)

#### **Hybrid Setup Process:**

1. Deploy FastAPI server to Railway/Render
2. Update OAuth buttons to use API domain
3. Handle CORS properly

---

## 🎯 **Recommended Implementation**

**I recommend Option 1 (Netlify)** because:

1. **Easiest migration** from GitHub Pages
2. **No code changes** to your existing FastAPI OAuth logic
3. **Free tier** handles most use cases
4. **Built-in analytics** and deployment previews
5. **Custom domain** support with SSL

## 🚀 **Next Steps**

**Choose your preferred option and I'll help you implement it!**

1. **Netlify** - I can help you deploy and configure everything
1. **Auth0** - I can integrate it into your existing site
1. **Vercel** - I can create the serverless functions
1. **Hybrid** - I can help deploy your FastAPI server

**Which option would you like to implement?**
