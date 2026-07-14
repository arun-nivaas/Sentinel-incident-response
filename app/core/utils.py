import hashlib

def compute_fingerprint(service_name: str | None, error_type: str | None, endpoint: str | None) -> str:
    key = f"{service_name or ''}|{error_type or ''}|{endpoint or ''}".lower().strip()
    return hashlib.sha256(key.encode()).hexdigest()[:16]