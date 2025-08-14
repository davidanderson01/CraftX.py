import json
import os
import pathlib

from eth_account import Account
from solcx import compile_standard, install_solc, set_solc_version
from web3 import Web3

RPC_URL = os.environ["RPC_URL"]
RPC_AUTH_TOKEN = os.environ.get("RPC_AUTH_TOKEN", "")
PRIVATE_KEY = os.environ["PRIVATE_KEY"]

ROOT = pathlib.Path(__file__).resolve().parents[1]
sol_path = ROOT / "contracts" / "CraftXAttestation.sol"
source = sol_path.read_text()

SOLC_VERSION = "0.8.24"
install_solc(SOLC_VERSION)
set_solc_version(SOLC_VERSION)

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

headers = {"Authorization": f"Bearer {RPC_AUTH_TOKEN}"} if RPC_AUTH_TOKEN else {}
w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={"headers": headers}))
assert w3.is_connected(), "RPC not reachable"

acct = Account.from_key(PRIVATE_KEY)
deployer = acct.address
chain_id = w3.eth.chain_id

contract = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(deployer)
tx = contract.constructor().build_transaction({
    "from": deployer,
    "nonce": nonce,
    "chainId": chain_id,
    "type": 2,
    "maxPriorityFeePerGas": w3.to_wei(2, "gwei"),
    "maxFeePerGas": w3.eth.gas_price * 2,
})
signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
print("Deploy tx:", tx_hash.hex())
rcpt = w3.eth.wait_for_transaction_receipt(tx_hash)
addr = rcpt.contractAddress
print("Deployed:", addr)

# Save ABI
out = ROOT / "artifacts"
out.mkdir(exist_ok=True)
(out / "CraftXAttestation.abi.json").write_text(json.dumps(abi, indent=2))
print("ABI saved to artifacts/CraftXAttestation.abi.json")
