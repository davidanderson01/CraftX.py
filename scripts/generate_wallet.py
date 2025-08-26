#!/usr/bin/env python3
"""
CraftX Ethereum Wallet Generator for Zero-Cost Anchoring
Generates a Sepolia testnet wallet for attestation anchoring.
"""

import os
import secrets
from eth_account import Account


def generate_ethereum_wallet():
    """Generate a new Ethereum wallet for Sepolia testnet."""

    # Generate a random 32-byte private key using secrets for cryptographic security
    private_key_bytes = secrets.token_bytes(32)

    # Create account from private key
    account = Account.from_key(private_key_bytes)

    print("🔑 ETHEREUM WALLET GENERATED:")
    print("=" * 60)
    print(f"Address: {account.address}")
    print(f"Private Key: {account.key.hex()}")
    print(f"Network: Sepolia Testnet")
    print("")
    print("⚠️  SECURITY NOTES:")
    print("1. Keep private key secure - never commit to git")
    print("2. Add to GitHub Secrets as ETHEREUM_PRIVATE_KEY")
    print("3. This is for TESTNET ONLY - never use for mainnet")
    print("")
    print("📍 GET FREE SEPOLIA ETH:")
    print("• https://sepoliafaucet.com/")
    print("• https://faucet.sepolia.dev/")
    print("• https://sepolia-faucet.pk910.de/")
    print("")
    print("🔧 NEXT STEPS:")
    print("1. Copy private key to GitHub Secrets")
    print("2. Deploy attestation smart contract")
    print("3. Set up Cloudflare Gateway CNAME")

    return account.key.hex()


if __name__ == "__main__":
    generate_ethereum_wallet()
