# Apple OAuth Environment Variables Setup Script
# Run this in PowerShell to get your environment variables formatted for Netlify

Write-Host "🍎 Setting up Apple OAuth Environment Variables for CraftX.py" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

# Check if private key file exists
$privateKeyPath = "C:\Users\david\Downloads\AuthKey_CraftX.p8"

if (Test-Path $privateKeyPath) {
    Write-Host "✅ Found private key file at: $privateKeyPath" -ForegroundColor Green
    Write-Host ""
    
    # Read the private key content
    $privateKey = Get-Content $privateKeyPath -Raw
    
    Write-Host "📋 Copy these EXACT values to your Netlify Environment Variables:" -ForegroundColor Yellow
    Write-Host "=" * 70 -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "Variable Name: APPLE_CLIENT_ID" -ForegroundColor Cyan
    Write-Host "Value: org.craftx.oauth.web" -ForegroundColor White
    Write-Host ""
    
    Write-Host "Variable Name: APPLE_TEAM_ID" -ForegroundColor Cyan  
    Write-Host "Value: CZVXX792P5" -ForegroundColor White
    Write-Host ""
    
    Write-Host "Variable Name: APPLE_KEY_ID" -ForegroundColor Cyan
    Write-Host "Value: X3787Y7BAX" -ForegroundColor White
    Write-Host ""
    
    Write-Host "Variable Name: APPLE_PRIVATE_KEY" -ForegroundColor Cyan
    Write-Host "Value:" -ForegroundColor White
    Write-Host $privateKey -ForegroundColor Green
    Write-Host ""
    
    Write-Host "=" * 70 -ForegroundColor Gray
    Write-Host "🚀 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Go to https://app.netlify.com/" -ForegroundColor White
    Write-Host "2. Select your CraftX.py site (harmonious-naiad-3cd735)" -ForegroundColor White
    Write-Host "3. Go to Site settings → Environment variables" -ForegroundColor White
    Write-Host "4. Add each of the 4 variables above" -ForegroundColor White
    Write-Host "5. Save and redeploy your site" -ForegroundColor White
    Write-Host "6. Test Apple Sign In at your live site!" -ForegroundColor White
    Write-Host ""
    Write-Host "✅ Your Apple OAuth will be fully functional!" -ForegroundColor Green
    
}
else {
    Write-Host "❌ Private key file not found at: $privateKeyPath" -ForegroundColor Red
    Write-Host "Please check the file path and try again." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "You can still manually copy the private key content:" -ForegroundColor Cyan
    Write-Host "1. Open the .p8 file in a text editor" -ForegroundColor White
    Write-Host "2. Copy the entire content (including -----BEGIN/END----- lines)" -ForegroundColor White
    Write-Host "3. Use that as the APPLE_PRIVATE_KEY value in Netlify" -ForegroundColor White
}

Write-Host ""
Write-Host "🍎 Apple OAuth Configuration Complete!" -ForegroundColor Green
