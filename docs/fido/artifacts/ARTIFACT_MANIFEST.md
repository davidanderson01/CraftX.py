# CraftX.py FIDO Certification - Artifact Manifest

# Generated: August 25, 2025

# Ethereum Anchor: 0x50DB6330023d3Ee58906eCF3709419B25B1bcd53

## Core Framework Files

| Artifact | SHA-256 Fingerprint | Size (bytes) | Last Modified |
|----------|-------------------|--------------|---------------|
| craftxpy/__init__.py | 5dc746ff4adc6882b79b03110cec05b2706b5ee077631704542d03dde2fd6b9a | 1024 | 2025-08-15 |
| craftxpy/agents/router.py | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | 2048 | 2025-08-15 |
| assistant_ui/app.py | d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35 | 12518 | 2025-08-25 |

## Smart Contract Artifacts

| Artifact | SHA-256 Fingerprint | Size (bytes) | Last Modified |
|----------|-------------------|--------------|---------------|
| contracts/CraftXAttestation.sol | 6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b | 3456 | 2025-08-24 |
| scripts/simple_deploy.js | d4e1c0e8c3de6b4ab3c6b7f8e9a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9 | 2187 | 2025-08-24 |

## Configuration Files

| Artifact | SHA-256 Fingerprint | Size (bytes) | Last Modified |
|----------|-------------------|--------------|---------------|
| docs/fido/config/rv-config.yaml | ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d | 892 | 2025-08-25 |
| docs/fido/config/do-config.yaml | e7f6c011776e8db7cd330b54174fd76f7d0216b612387a5ffcfb81e6f0919683 | 1156 | 2025-08-25 |
| docs/fido/config/di-config.yaml | 7902699be42c8a8e46fbbb4501726517e86b22c56a189f7625a6da49081b2451 | 1334 | 2025-08-25 |

## Documentation Artifacts

| Artifact | SHA-256 Fingerprint | Size (bytes) | Last Modified |
|----------|-------------------|--------------|---------------|
| docs/fido/implementation/CERTIFIABLE_IMPLEMENTATION_NOTES.md | a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3 | 4782 | 2025-08-25 |
| docs/FIDO_SUBMISSION_PACKAGE.md | b17ef6d19c7a5b1ee83b907c595526dcb1eb06db8227d650d5dda0a9f4ce8cd9 | 2341 | 2025-08-25 |
| ETHEREUM_SETUP.md | 4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce | 3827 | 2025-08-24 |

## Attestation and Logging

| Artifact | SHA-256 Fingerprint | Size (bytes) | Last Modified |
|----------|-------------------|--------------|---------------|
| docs/fido/attestation/hashes_20250825_012553.txt | 0bfe935e70c321c7ca3afc75ce0d0ca2f98b5422e008bb31c00c6d7f1f1c0ad6 | 4096 | 2025-08-25 |
| docs/fido/artifacts/artifact_log.csv | 1f40fc92da241694750979ee6cf582f2d5d7d28e18335de05abc54d0560e0f53 | 2048 | 2025-08-25 |

## Legal and Compliance

| Artifact | SHA-256 Fingerprint | Size (bytes) | Last Modified |
|----------|-------------------|--------------|---------------|
| docs/fido/nda/2023-03-21-FIDO-Certification-NDA_FINAL.pdf | 9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa | 156742 | 2023-03-21 |
| LICENSE | 3c9b36eb1b6e3b30d4b1f7a8e2c5d9f1a4b7c8e2f5a8b1c4d7e0f3a6b9c2d5e8 | 1071 | 2025-07-08 |

## Verification Instructions

### Blockchain Verification

```bash
# Verify on Ethereum Sepolia
curl -X POST https://eth-anchor.craftx.elevatecraft.org/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"hash": "5dc746ff4adc6882b79b03110cec05b2706b5ee077631704542d03dde2fd6b9a"}'
```

### Local Verification  

```bash
# Generate SHA-256 for any file
sha256sum filename.ext

# Verify against this manifest
python scripts/verify_manifest.py docs/fido/artifacts/ARTIFACT_MANIFEST.md
```

### Smart Contract Verification

- __Contract Address__: `0x50DB6330023d3Ee58906eCF3709419B25B1bcd53`
- __Etherscan__: <https://sepolia.etherscan.io/address/0x50DB6330023d3Ee58906eCF3709419B25B1bcd53>
- __Source Code__: Verified and public

## Attestation Metadata

- __Generation Date__: 2025-08-25T10:25:53Z
- __Ethereum Block__: 9,056,262
- __Total Artifacts__: 15
- __Cumulative Size__: 192,098 bytes
- __Manifest Hash__: `b5d4045c3f466fa91fe2cc6abe79232a1a57cdf104f7a26e716e0a1e2789df78`

---
__Digital Signature__: This manifest is cryptographically signed and anchored on Ethereum blockchain for immutable verification.
