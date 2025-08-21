# 🔧 OAuth Button Troubleshooting Guide

## 🎯 **Quick Diagnosis**

### **Test 1: Where are you accessing the site?**

1. **If testing locally** (like `file:///` or `localhost:8000`):
   - ❌ OAuth buttons won't work without a server
   - ✅ Need to deploy to Netlify first

2. **If on GitHub Pages** (`*.github.io`):
   - ❌ OAuth buttons won't work (static hosting only)
   - ✅ Need to move to Netlify for serverless functions

3. **If on Netlify** (`*.netlify.app`):
   - ✅ Should work if properly configured
   - ⚠️ Need environment variables set

## 🚀 **Solutions by Scenario**

### **Scenario A: Testing Locally**

**Problem**: Clicking OAuth buttons gives 404 or nothing happens

**Solution**: Deploy to Netlify first

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy your site
netlify deploy --prod --dir=.
```

### **Scenario B: On GitHub Pages**

**Problem**: OAuth buttons don't work on static hosting

**Solution**: Move to Netlify (supports serverless functions)

1. Connect your GitHub repo to Netlify
2. Configure build settings
3. Add environment variables

### **Scenario C: On Netlify but Not Working**

**Problem**: Buttons redirect but get errors

**Likely Causes**:

1. Environment variables not set
2. OAuth providers not configured
3. Serverless functions not deployed

**Solution**: Configure environment variables

```bash
netlify env:set GOOGLE_CLIENT_ID "your_google_client_id"
netlify env:set GOOGLE_CLIENT_SECRET "your_google_client_secret"
# ... add all OAuth providers
```

## 🔧 **Immediate Debug Steps**

### **Step 1: Check Console Errors**

1. Open browser DevTools (F12)
2. Go to Console tab
3. Click an OAuth button
4. Look for error messages

### **Step 2: Check Network Tab**

1. Open DevTools → Network tab
2. Click an OAuth button
3. See what request is made
4. Check if it returns 404, 500, or other errors

### **Step 3: Test Button Click**

Add this to your browser console to test:

```javascript
// Test if buttons are properly attached
document.querySelectorAll('.btn-oauth').forEach((btn, i) => {
    console.log(`Button ${i}:`, btn.dataset.provider, btn.onclick);
});

// Test manual OAuth redirect
console.log('Hostname:', window.location.hostname);
console.log('Has serverless functions:', 
    window.location.hostname === 'craftx.elevatecraft.org' ||
    window.location.hostname.includes('netlify.app')
);
```

## 🎯 **Most Likely Issues**

1. **Testing locally without server** (90% of cases)
2. **Missing environment variables on Netlify** (8% of cases)
3. **Incorrect redirect URIs in OAuth providers** (2% of cases)

## 🚀 **Quick Fix Options**

### **Option 1: Deploy to Netlify (Recommended)**

```bash
# If you have Netlify account
1. Go to netlify.com
2. "Add new site" → "Import from Git"
3. Connect your GitHub repo
4. Deploy settings: Build command: (leave empty), Publish directory: "."
5. Add environment variables in Site Settings
```

### **Option 2: Test with Local Server**

```bash
# Simple Python server
python -m http.server 8000

# Or Node.js server
npx http-server
```

### **Option 3: Use Live Preview**

- If using VS Code: Install "Live Server" extension
- Right-click index.html → "Open with Live Server"

Let me know:

1. **Where are you testing?** (localhost, GitHub Pages, Netlify, etc.)
2. **What happens when you click a button?** (nothing, 404, error message)
3. **Any console errors?** (check F12 DevTools)

Then I can give you the exact fix! 🎯
