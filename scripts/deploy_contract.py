#!/usr/bin/env python3
"""
Deploy CraftX Attestation Smart Contract to Sepolia
"""

import os
from web3 import Web3
from eth_account import Account

# Smart contract source code
CONTRACT_SOURCE = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract CraftXAttestation {
    struct Attestation {
        bytes32 hash;
        uint256 timestamp;
        string buildId;
        address attester;
    }
    
    mapping(bytes32 => Attestation) public attestations;
    bytes32[] public attestationHashes;
    
    event AttestationStored(
        bytes32 indexed hash,
        uint256 timestamp,
        string buildId,
        address indexed attester
    );
    
    function storeAttestation(
        bytes32 _hash,
        string memory _buildId
    ) external {
        require(_hash != bytes32(0), "Invalid hash");
        require(bytes(_buildId).length > 0, "Invalid build ID");
        
        attestations[_hash] = Attestation({
            hash: _hash,
            timestamp: block.timestamp,
            buildId: _buildId,
            attester: msg.sender
        });
        
        attestationHashes.push(_hash);
        
        emit AttestationStored(_hash, block.timestamp, _buildId, msg.sender);
    }
    
    function getAttestation(bytes32 _hash) external view returns (
        bytes32 hash,
        uint256 timestamp,
        string memory buildId,
        address attester
    ) {
        Attestation memory att = attestations[_hash];
        return (att.hash, att.timestamp, att.buildId, att.attester);
    }
    
    function getAttestationCount() external view returns (uint256) {
        return attestationHashes.length;
    }
}
'''


def deploy_contract():
    """Deploy the attestation contract to Sepolia."""

    print("🚀 DEPLOYING CRAFTX ATTESTATION CONTRACT")
    print("=" * 50)

    # Get private key
    private_key = os.getenv('ETHEREUM_PRIVATE_KEY')
    if not private_key:
        print("❌ ETHEREUM_PRIVATE_KEY not found")
        return

    account = Account.from_key(private_key)
    print(f"Deploying from: {account.address}")

    # Contract bytecode (compiled)
    # This would normally come from solc compilation
    print("\n📋 MANUAL DEPLOYMENT INSTRUCTIONS:")
    print("1. Use VS Code deployment script: node scripts/simple_deploy.js")
    print("2. Create new file: CraftXAttestation.sol")
    print("3. Paste the contract code")
    print("4. Compile with Solidity 0.8.19+")
    print("5. Deploy to Sepolia network")
    print("6. Copy contract address to update CI workflow")

    print(f"\n🔑 Use this address for deployment: {account.address}")
    print(f"🔑 Private key is in environment variable")

    # Save contract source to file for easy access
    with open('contracts/CraftXAttestation.sol', 'w') as f:
        f.write(CONTRACT_SOURCE)

    print(f"\n✅ Contract source saved to: contracts/CraftXAttestation.sol")
    print("\n🎯 After deployment, update .github/workflows/ci.yml with contract address")


if __name__ == "__main__":
    deploy_contract()
