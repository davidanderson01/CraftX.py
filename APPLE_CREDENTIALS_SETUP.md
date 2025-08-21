# 🍎 Apple OAuth Configuration for CraftX.py

## ✅ **Your Apple Credentials**

Based on the information you provided:

- **Key ID**: `X3787Y7BAX`
- **Team ID**: `CZVXX792P5`
- **Private Key File**: `C:\Users\david\Downloads\AuthKey_CraftX.p8`
- **Client ID**: `org.craftx.oauth.web` (from your Services ID)

## 🔧 **Netlify Environment Variables Setup**

### **Method 1: Netlify Dashboard (Recommended)**

1. Go to [Netlify Dashboard](https://app.netlify.com/)
2. Select your CraftX.py site (harmonious-naiad-3cd735)
3. Go to **Site settings** → **Environment variables**
4. Add these **exact** variables:

```env
APPLE_CLIENT_ID=org.craftx.oauth.web
APPLE_TEAM_ID=CZVXX792P5
APPLE_KEY_ID=X3787Y7BAX
```

### **For APPLE_PRIVATE_KEY**

1. Open `C:\Users\david\Downloads\AuthKey_CraftX.p8` in a text editor
2. Copy the **entire contents** (including the header and footer lines)
3. The content should look like:

   ```text
   -----BEGIN PRIVATE KEY-----
   MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQg...
   (multiple lines of base64 encoded data)
   ...
   -----END PRIVATE KEY-----
   ```

4. In Netlify, add environment variable:
   - **Key**: `APPLE_PRIVATE_KEY`
   - **Value**: Paste the entire private key content (with headers)

### **Method 2: Copy Private Key Content**

You can also run this PowerShell command to get the private key content:

```powershell
Get-Content "C:\Users\david\Downloads\AuthKey_CraftX.p8" | Out-String
```

Then copy the output and paste it as the `APPLE_PRIVATE_KEY` value in Netlify.

## 🚀 **Quick Setup Script**

Here's a script to help you set up the environment variables:

### **PowerShell Script**

```powershell
# Read the private key content
$privateKey = Get-Content "C:\Users\david\Downloads\AuthKey_CraftX.p8" -Raw

Write-Host "🍎 Apple OAuth Environment Variables for Netlify:" -ForegroundColor Green
Write-Host ""
Write-Host "APPLE_CLIENT_ID=org.craftx.oauth.web" -ForegroundColor Yellow
Write-Host "APPLE_TEAM_ID=CZVXX792P5" -ForegroundColor Yellow  
Write-Host "APPLE_KEY_ID=X3787Y7BAX" -ForegroundColor Yellow
Write-Host ""
Write-Host "APPLE_PRIVATE_KEY=" -ForegroundColor Yellow -NoNewline
Write-Host $privateKey -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Copy these values to your Netlify environment variables!" -ForegroundColor Green
```

## 🔄 **After Setting Environment Variables**

1. **Save** all environment variables in Netlify
2. **Redeploy** your site (should auto-deploy when you save env vars)
3. **Test** Apple Sign In at: <https://harmonious-naiad-3cd735.netlify.app>
4. **Check logs** in Netlify if there are any issues

## 🎯 **Apple Developer Console Verification**

Make sure your Apple Developer Console is configured with:

- **Services ID**: `org.craftx.oauth.web`
- **Return URL**: `https://harmonious-naiad-3cd735.netlify.app/.netlify/functions/oauth-handler/callback/apple`
- **Web Domain**: `harmonious-naiad-3cd735.netlify.app`

## 🔍 **Testing**

Once configured, your Apple Sign In button should:

1. **Redirect** to Apple's authentication page
2. **Show** Apple's privacy consent screen
3. **Return** to your site with user authentication
4. **Display** success message with user info

## 🆘 **Troubleshooting**

If Apple Sign In doesn't work:

1. **Check Netlify logs** for error messages
2. **Verify** all environment variables are set correctly
3. **Confirm** Apple Developer Console configuration
4. **Test** other OAuth providers to ensure the flow works

Your Apple OAuth is ready to go once you add these environment variables to Netlify!
