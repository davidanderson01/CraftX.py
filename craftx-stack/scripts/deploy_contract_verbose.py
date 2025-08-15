#!/usr/bin/env python3
"""Deploy CraftX Attestation contract with explicit .env loading"""

import json
import os
import pathlib
from dotenv import load_dotenv

from eth_account import Account
from solcx import compile_standard, install_solc, set_solc_version
from web3 import Web3

# Load .env file explicitly
ROOT = pathlib.Path(__file__).resolve().parents[1]
env_path = ROOT / ".env"
print(f"Loading environment from: {env_path}")
load_dotenv(env_path)

# Verify environment variables
RPC_URL = os.environ.get("RPC_URL")
RPC_AUTH_TOKEN = os.environ.get("RPC_AUTH_TOKEN", "")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")

print(f"RPC_URL: {RPC_URL}")
print(f"RPC_AUTH_TOKEN: {'***' if RPC_AUTH_TOKEN else 'NOT_SET'}")
print(
    f"PRIVATE_KEY: {'***' + PRIVATE_KEY[-10:] if PRIVATE_KEY else 'NOT_SET'}")

if not RPC_URL:
    raise ValueError("RPC_URL not set in .env file")
if not PRIVATE_KEY:
    raise ValueError("PRIVATE_KEY not set in .env file")

sol_path = ROOT / "contracts" / "CraftXAttestation.sol"
source = sol_path.read_text()

SOLC_VERSION = "0.8.24"
print(f"Installing Solidity {SOLC_VERSION}...")
install_solc(SOLC_VERSION)
set_solc_version(SOLC_VERSION)

print("Compiling contract...")
compiled = compile_standard(
    {
        "language": "Solidity",
        "sources": {"CraftXAttestation.sol": {"content": source}},
        "settings": {
            "optimizer": {"enabled": True, "runs": 200},
            "outputSelection": {"*": {"*": ["abi", "evm.bytecode.object"]}},
        },
    }
)
abi = compiled["contracts"]["CraftXAttestation.sol"]["CraftXAttestation"]["abi"]
bytecode = compiled["contracts"]["CraftXAttestation.sol"]["CraftXAttestation"]["evm"]["bytecode"]["object"]

print("Connecting to RPC...")
headers = {"Authorization": f"Bearer {RPC_AUTH_TOKEN}"} if RPC_AUTH_TOKEN else {}
w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={"headers": headers}))

if not w3.is_connected():
    raise ConnectionError(f"Cannot connect to RPC: {RPC_URL}")

print("RPC connected successfully!")

acct = Account.from_key(PRIVATE_KEY)
deployer = acct.address
chain_id = w3.eth.chain_id

print(f"Deployer address: {deployer}")
print(f"Chain ID: {chain_id}")

# Check account balance
balance = w3.eth.get_balance(deployer)
print(f"Account balance: {w3.from_wei(balance, 'ether')} ETH")

if balance == 0:
    print("⚠️  WARNING: Account has 0 ETH balance. You need testnet ETH to deploy.")
    print("   For testnets, get free ETH from a faucet.")

contract = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(deployer)

print("Building transaction...")
tx = contract.constructor().build_transaction({
    "from": deployer,
    "nonce": nonce,
    "chainId": chain_id,
    "type": 2,
    "maxPriorityFeePerGas": w3.to_wei(2, "gwei"),
    "maxFeePerGas": w3.eth.gas_price * 2,
})

print(f"Estimated gas: {tx['gas']}")
print("Signing and sending transaction...")

signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
print(f"Deploy tx: {tx_hash.hex()}")

print("Waiting for transaction receipt...")
rcpt = w3.eth.wait_for_transaction_receipt(tx_hash)
addr = rcpt.contractAddress
print(f"✅ Contract deployed at: {addr}")

# Save ABI
out = ROOT / "artifacts"
out.mkdir(exist_ok=True)
(out / "CraftXAttestation.abi.json").write_text(json.dumps(abi, indent=2))
print("📁 ABI saved to artifacts/CraftXAttestation.abi.json")

# Update .env file with contract address
env_content = env_path.read_text()
updated_content = env_content.replace(
    "CONTRACT_ADDRESS=0x<CONTRACT_ADDRESS>",
    f"CONTRACT_ADDRESS={addr}"
)
env_path.write_text(updated_content)
print(f"📝 Updated .env with CONTRACT_ADDRESS={addr}")

print("\n🎉 Deployment complete!")
print(f"Contract Address: {addr}")
print(f"Transaction Hash: {tx_hash.hex()}")
print(f"Gas Used: {rcpt.gasUsed}")
