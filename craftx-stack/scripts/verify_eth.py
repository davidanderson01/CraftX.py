import hashlib
import os

from eth_account import Account
from eth_account.messages import encode_defunct

# Simple verifier: verifies an Ethereum signature over a message and checks a fingerprint marker
# Usage: set environment variable FINGERPRINT to expected fingerprint, then call verify_signature(message, signature, signer_address)

EXPECTED_FINGERPRINT = os.getenv('FINGERPRINT')


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_signature(message: str, signature: str, signer_address: str) -> bool:
    msg = encode_defunct(text=message)
    try:
        recovered = Account.recover_message(msg, signature=signature)
        return recovered.lower() == signer_address.lower()
    except Exception:
        return False


def extract_fingerprint(text: str) -> str:
    # look for 'Fingerprint: <id>' in text
    for line in text.splitlines():
        if 'Fingerprint:' in line:
            return line.split('Fingerprint:')[-1].strip()
    return ''


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 4:
        print('Usage: python verify_eth.py <message-file> <signature> <signer-address>')
        sys.exit(2)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        msg = f.read()
    sig = sys.argv[2]
    signer = sys.argv[3]
    ok = verify_signature(msg, sig, signer)
    fp = extract_fingerprint(msg)
    print('signature_ok=', ok)
    print('fingerprint=', fp)
    if EXPECTED_FINGERPRINT:
        print('fingerprint_matches_expected=', fp == EXPECTED_FINGERPRINT)
