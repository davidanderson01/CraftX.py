import datetime
import hashlib
import json
import os
import pathlib

from eth_account import Account
from web3 import Web3

RPC_URL = os.environ["RPC_URL"]
RPC_AUTH_TOKEN = os.environ.get("RPC_AUTH_TOKEN", "")
PRIVATE_KEY = os.environ["PRIVATE_KEY"]
CONTRACT_ADDRESS = os.environ["CONTRACT_ADDRESS"]
FINGERPRINT = os.environ["FINGERPRINT"]
MODELFILE_PATH = os.environ.get("MODELFILE_PATH", "./Modelfile")
OFFCHAIN_URI = os.environ.get("OFFCHAIN_URI", "")

ARTIFACT_ABI = os.environ.get(
    "ABI_PATH", "./artifacts/CraftXAttestation.abi.json")
abi = json.loads(pathlib.Path(ARTIFACT_ABI).read_text())

headers = {"Authorization": f"Bearer {RPC_AUTH_TOKEN}"} if RPC_AUTH_TOKEN else {}
w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={"headers": headers}))
assert w3.is_connected(), "RPC not reachable"

acct = Account.from_key(PRIVATE_KEY)
publisher = acct.address
chain_id = w3.eth.chain_id
contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)


def sha256_bytes32(data: bytes) -> bytes:
    h = hashlib.sha256(data).digest()
    assert len(h) == 32
    return h


model_bytes = pathlib.Path(MODELFILE_PATH).read_bytes()
model_hash_b32 = sha256_bytes32(model_bytes)

container_id = ""
try:
    container_id = pathlib.Path("/proc/1/cpuset").read_text().strip()
except Exception:
    container_id = ""
container_hash_b32 = sha256_bytes32(
    container_id.encode()) if container_id else b"\x00" * 32

fingerprint_hash = w3.keccak(text=FINGERPRINT)
date = int(datetime.datetime.utcnow().strftime("%Y%m%d"))

nonce = w3.eth.get_transaction_count(publisher)
tx = contract.functions.attest(
    fingerprint_hash,
    date,
    model_hash_b32,
    container_hash_b32,
    OFFCHAIN_URI
).build_transaction({
    "from": publisher,
    "nonce": nonce,
    "chainId": chain_id,
    "type": 2,
    "maxPriorityFeePerGas": w3.to_wei(2, "gwei"),
    "maxFeePerGas": w3.eth.gas_price * 2,
})
signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
print("Anchor tx:", tx_hash.hex())
rcpt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Confirmed in block", rcpt.blockNumber)
