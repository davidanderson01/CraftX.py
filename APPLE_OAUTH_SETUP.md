# 🍎 Apple Sign In Setup Guide for CraftX.py

## ✅ **Quick Setup Summary**

Your Apple OAuth integration is now **code-complete** and ready! Here's what you need to do:

## 🔑 **Required Information**

You'll need these from Apple Developer Console:

```env
APPLE_CLIENT_ID=org.craftx.oauth.web
APPLE_TEAM_ID=YOUR_10_CHAR_TEAM_ID
APPLE_KEY_ID=YOUR_10_CHAR_KEY_ID
APPLE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----
YOUR_PRIVATE_KEY_CONTENT_HERE
-----END PRIVATE KEY-----
```

## 📋 **Step-by-Step Apple Developer Console Setup**

### **Step 1: Create App ID**

1. Go to [Apple Developer Console](https://developer.apple.com/account/) → Certificates, Identifiers & Profiles
2. Click "Identifiers" → "+" button
3. Select "App IDs" → "App" → Continue
4. Fill out:
   - **Description**: `CraftX.py OAuth Application`
   - **Bundle ID**: `org.craftx.oauth`
   - **Capabilities**: ✅ Check "Sign In with Apple"
5. Register

### **Step 2: Create Services ID (Web Auth)**

1. Back to "Identifiers" → "+" button
2. Select "Services IDs" → Continue
3. Fill out:
   - **Description**: `CraftX.py Web Authentication`
   - **Identifier**: `org.craftx.oauth.web`
4. Register

### **Step 3: Configure Services ID**

1. Click on your Services ID → Edit
2. ✅ Check "Sign In with Apple"
3. Click "Configure"
4. Set:
   - **Primary App ID**: Select `org.craftx.oauth` from Step 1
   - **Web Domain**: `harmonious-naiad-3cd735.netlify.app`
   - **Return URLs**:

     ```text
     https://harmonious-naiad-3cd735.netlify.app/.netlify/functions/oauth-handler/callback/apple
     ```

5. Save → Continue → Save

### **Step 4: Create Private Key**

1. Go to "Keys" → "+" button
2. Fill out:
   - **Key Name**: `CraftX.py Sign In with Apple Key`
   - **Services**: ✅ Check "Sign In with Apple"
3. Click "Configure" → Select your App ID from Step 1
4. Save → Continue → Register
5. **⚠️ IMPORTANT**: Download the `.p8` file (you can only download this ONCE!)
6. **Note the Key ID** (10-character string)

### **Step 5: Get Team ID**

1. Go to "Membership" in sidebar
2. Copy your **Team ID** (10-character string)

## 🌐 **Netlify Environment Setup**

Add these environment variables to your Netlify site:

1. Go to [Netlify Dashboard](https://app.netlify.com/) → Your site
2. Site settings → Environment variables
3. Add each variable:

```env
APPLE_CLIENT_ID=org.craftx.oauth.web
APPLE_TEAM_ID=YOUR_TEAM_ID_HERE
APPLE_KEY_ID=YOUR_KEY_ID_HERE
APPLE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----
PASTE_YOUR_PRIVATE_KEY_CONTENT_HERE
-----END PRIVATE KEY-----
```

## ✅ **What's Already Implemented**

Your Apple OAuth is **100% code-complete**:

- ✅ **OAuth Handler**: Full Apple Sign In implementation with JWT authentication
- ✅ **Private Key Handling**: Secure JWT creation for Apple's requirements
- ✅ **Token Exchange**: Complete authorization code → access token flow
- ✅ **User Data Extraction**: Email, name, and user ID from Apple ID token
- ✅ **Error Handling**: Comprehensive error messages for debugging
- ✅ **Security**: ES256 algorithm with proper Apple JWT requirements

## 🔄 **Apple OAuth Flow**

1. **User clicks Apple button** → Redirects to Apple Sign In
2. **Apple authenticates user** → Returns to your callback URL
3. **Your function receives code** → Creates JWT client secret
4. **Exchanges code for tokens** → Gets Apple ID token
5. **Extracts user info** → Returns user data to your frontend

## 🚦 **Testing Your Apple Integration**

Once you've completed the Apple Developer Console setup:

1. **Add environment variables** to Netlify
2. **Redeploy** your site (or wait for auto-deploy from git push)
3. **Test** the Apple button on your live site: <https://harmonious-naiad-3cd735.netlify.app>
4. **Check Netlify logs** for any errors during authentication

## 🔧 **Troubleshooting**

### **Common Issues:**

1. **"Invalid client" error**:
   - Check your `APPLE_CLIENT_ID` matches your Services ID
   - Verify the Services ID is configured for Sign In with Apple

2. **"Invalid key" error**:
   - Ensure private key format includes `-----BEGIN PRIVATE KEY-----` headers
   - Check `APPLE_KEY_ID` matches the key you created
   - Verify `APPLE_TEAM_ID` is correct

3. **"Invalid redirect_uri" error**:
   - Confirm the return URL in Apple Developer Console exactly matches:
     `https://harmonious-naiad-3cd735.netlify.app/.netlify/functions/oauth-handler/callback/apple`

## 💡 **Apple Sign In Benefits**

- **Privacy-focused**: Apple emphasizes user privacy
- **Secure**: Uses ES256 JWT authentication
- **Native integration**: Works seamlessly on iOS/macOS
- **Professional**: Trusted by enterprise applications

## 🎯 **Final Checklist**

- [ ] Create App ID in Apple Developer Console
- [ ] Create Services ID for web authentication
- [ ] Configure Services ID with your Netlify domain
- [ ] Create and download private key (.p8 file)
- [ ] Note your Team ID and Key ID
- [ ] Add all environment variables to Netlify
- [ ] Test Apple Sign In on your live site

Your Apple OAuth implementation is complete and ready to use once you finish the Apple Developer Console setup!
