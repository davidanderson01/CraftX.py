#!/usr/bin/env python3
"""Generate Ethereum account for CraftX deployment"""

from eth_account import Account
import secrets
from datetime import datetime

# Generate new account
account = Account.create()

# Generate fingerprint
date_str = datetime.now().strftime("%d%b%Y").upper()
random_id = secrets.token_urlsafe(8)[:10]

print("🔐 Generated new Ethereum account for CraftX:")
print(f"Address: {account.address}")
print(f"Private Key: {account.key.hex()}")
print()
print("📝 Copy these values to your .env file:")
print(f"PRIVATE_KEY={account.key.hex()}")
print(f"# Account address (for reference): {account.address}")
print(f"FINGERPRINT=craftx-sovereign-sig-v1-{date_str}-{random_id}")
print()
print("⚠️  SECURITY WARNING:")
print("- This is for TESTING ONLY")
print("- Never use this key with real funds")
print("- Keep your private key secure")
