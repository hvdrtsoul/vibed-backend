import base58
import nacl.signing
import nacl.exceptions

def verify_signature(public_key_b58: str, signature_b58: str, message: str) -> bool:
    try:
        public_key_bytes = base58.b58decode(public_key_b58)
        signature_bytes = base58.b58decode(signature_b58)
        verify_key = nacl.signing.VerifyKey(public_key_bytes)
        verify_key.verify(message.encode(), signature_bytes)
        return True
    except (ValueError, nacl.exceptions.BadSignatureError):
        return False
