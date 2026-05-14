// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract VeriVisionRegistry {
    struct VerificationRecord {
        string imageHash;
        string vlmModel;
        string verifierModel;
        uint256 objectCount;
        uint256 hallucinationCount;
        uint256 timestamp;
        address verifier;
        bool exists;
    }

    mapping(bytes32 => VerificationRecord) public records;
    bytes32[] public recordIds;

    event VerificationStored(
        bytes32 indexed recordId,
        string imageHash,
        uint256 hallucinationCount,
        address verifier
    );

    function storeVerification(
        string memory imageHash,
        string memory vlmModel,
        string memory verifierModel,
        uint256 objectCount,
        uint256 hallucinationCount
    ) external returns (bytes32) {
        bytes32 recordId = keccak256(
            abi.encodePacked(imageHash, vlmModel, block.timestamp, msg.sender)
        );

        require(!records[recordId].exists, "Record already exists");

        records[recordId] = VerificationRecord({
            imageHash: imageHash,
            vlmModel: vlmModel,
            verifierModel: verifierModel,
            objectCount: objectCount,
            hallucinationCount: hallucinationCount,
            timestamp: block.timestamp,
            verifier: msg.sender,
            exists: true
        });

        recordIds.push(recordId);

        emit VerificationStored(recordId, imageHash, hallucinationCount, msg.sender);

        return recordId;
    }

    function getRecord(bytes32 recordId) external view returns (VerificationRecord memory) {
        require(records[recordId].exists, "Record not found");
        return records[recordId];
    }

    function getRecordCount() external view returns (uint256) {
        return recordIds.length;
    }

    function getHallucinationRate(bytes32 recordId) external view returns (uint256) {
        require(records[recordId].exists, "Record not found");
        VerificationRecord memory r = records[recordId];
        if (r.objectCount == 0) return 0;
        return (r.hallucinationCount * 10000) / r.objectCount;
    }
}
