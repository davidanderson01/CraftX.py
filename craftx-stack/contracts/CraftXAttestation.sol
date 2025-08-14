// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract Ownable {
    address public owner;
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor() {
        owner = msg.sender;
        emit OwnershipTransferred(address(0), owner);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "Zero address");
        emit OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }
}

contract CraftXAttestation is Ownable {
    struct Record {
        bytes32 modelHash;
        bytes32 containerHash;
        uint64  timestamp;
        string  uri;
    }

    // fingerprintHash = keccak256(utf8(fingerprint_string))
    mapping(bytes32 => mapping(uint32 => Record)) private _records; // date as YYYYMMDD (UTC)
    mapping(bytes32 => address) public publisherFor;

    event PublisherSet(bytes32 indexed fingerprintHash, address indexed publisher);
    event Attested(
        bytes32 indexed fingerprintHash,
        uint32  indexed date,
        bytes32 modelHash,
        bytes32 containerHash,
        uint64  timestamp,
        string  uri
    );

    function setPublisher(bytes32 fingerprintHash, address publisher) external onlyOwner {
        publisherFor[fingerprintHash] = publisher;
        emit PublisherSet(fingerprintHash, publisher);
    }

    function recordExists(bytes32 fingerprintHash, uint32 date) public view returns (bool) {
        return _records[fingerprintHash][date].timestamp != 0;
    }

    function getRecord(bytes32 fingerprintHash, uint32 date)
        external
        view
        returns (Record memory)
    {
        return _records[fingerprintHash][date];
    }

    function attest(
        bytes32 fingerprintHash,
        uint32  date,
        bytes32 modelHash,
        bytes32 containerHash,
        string  calldata uri
    ) external {
        require(publisherFor[fingerprintHash] == msg.sender, "Unauthorized");
        require(modelHash != bytes32(0), "modelHash required");
        require(!recordExists(fingerprintHash, date), "Already attested");

        uint64 ts = uint64(block.timestamp);
        _records[fingerprintHash][date] = Record({
            modelHash: modelHash,
            containerHash: containerHash,
            timestamp: ts,
            uri: uri
        });

        emit Attested(fingerprintHash, date, modelHash, containerHash, ts, uri);
    }
}
