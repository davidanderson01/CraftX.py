from dotenv import load_dotenv
from web3 import Web3
import os

print("Testing CraftX deployment prerequisites...")

# Load environment
load_dotenv('.env')
rpc_url = os.environ.get('RPC_URL')
private_key = os.environ.get('PRIVATE_KEY')

print(f"RPC_URL: {rpc_url}")
print(
    f"PRIVATE_KEY: {'***' + private_key[-10:] if private_key else 'NOT_SET'}")

# Test RPC connection
print("Testing RPC connection...")
try:
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    connected = w3.is_connected()
    print(f"RPC connected: {connected}")
    if connected:
        print(f"Chain ID: {w3.eth.chain_id}")
        print(f"Latest block: {w3.eth.block_number}")
except Exception as e:
    print(f"RPC connection failed: {e}")

print("Test complete.")
