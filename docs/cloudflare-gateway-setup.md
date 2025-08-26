# CraftX Cloudflare Gateway Setup Guide

## Overview

Set up a free Cloudflare Ethereum Gateway for zero-cost blockchain access.

## Steps

### 1. Domain Setup (if using custom domain)

```bash
# Add CNAME record in Cloudflare DNS:
# Name: eth-anchor
# Target: cloudflare-eth.com (or appropriate Cloudflare gateway)
# Result: eth-anchor.craftx.elevatecraft.org → Ethereum RPC
```

### 2. Alternative: Direct Cloudflare Gateway

```bash
# Use Cloudflare's public gateway directly:
CLOUDFLARE_GATEWAY="https://cloudflare-eth.com/v1/sepolia"

# Update ci.yml:
env:
  CLOUDFLARE_GATEWAY: "https://cloudflare-eth.com/v1/sepolia"
```

### 3. Rate Limiting Considerations

- Cloudflare provides generous free tier
- For production: consider upgrading or multiple gateways
- Implement exponential backoff in CI scripts

### 4. Testing Gateway Connection

```javascript
// Test script to verify gateway works
const { ethers } = require('ethers');

async function testGateway() {
  try {
    const provider = new ethers.JsonRpcProvider('https://your-gateway-url');
    const blockNumber = await provider.getBlockNumber();
    console.log('✅ Gateway connected! Latest block:', blockNumber);
  } catch (error) {
    console.error('❌ Gateway failed:', error.message);
  }
}

testGateway();
```

## Configuration Summary

### Required Environment Variables

```yaml
env:
  ETHEREUM_NETWORK: sepolia
  CLOUDFLARE_GATEWAY: "https://cloudflare-eth.com/v1/sepolia"  # Or your custom domain
  ATTESTATION_CONTRACT: "0xYourDeployedContractAddress"
```

### GitHub Secrets Needed

```bash
ETHEREUM_PRIVATE_KEY=0xYourGeneratedPrivateKey
LEDGER_PAT=ghp_YourPersonalAccessToken  # For attestation repo
```

## Next Steps

1. Deploy smart contract to get contract address
2. Generate Ethereum wallet for CI
3. Fund wallet with free Sepolia ETH from faucets
4. Test full pipeline with a commit to main branch
