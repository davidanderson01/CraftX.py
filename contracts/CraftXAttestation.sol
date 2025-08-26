
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
