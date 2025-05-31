import hashlib
def hash_license_key(license_key: str) -> str:
    return hashlib.sha256(license_key.encode()).hexdigest()

def decode_license_key(license_key: str) -> str:
    return hashlib.sha256(license_key.encode()).hexdigest()