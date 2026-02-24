"""
canonicalize.py

Small utility to canonicalize JSON-like dicts so they serialize deterministically.
Usage:
    python canonicalize.py
"""

import json
import hashlib

def canonicalize(obj):
    """
    Recursively sort dictionaries by key and produce a deterministic JSON string.
    """
    if isinstance(obj, dict):
        # sort keys and canonicalize values
        return {k: canonicalize(obj[k]) for k in sorted(obj.keys())}
    if isinstance(obj, list):
        return [canonicalize(v) for v in obj]
    return obj

def canonical_json(obj):
    c = canonicalize(obj)
    return json.dumps(c, separators=(',', ':'), ensure_ascii=False)

def sha256_of(obj):
    s = canonical_json(obj).encode('utf-8')
    return hashlib.sha256(s).hexdigest()

if __name__ == "__main__":
    sample = {
        "amount": 100,
        "reason": "refund",
        "metadata": {"user": "alice", "timestamp": "2026-02-xx"}
    }
    print("Canonical JSON:")
    print(canonical_json(sample))
    print("SHA256:")
    print(sha256_of(sample))
