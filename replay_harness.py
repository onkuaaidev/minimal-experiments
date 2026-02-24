"""
replay_harness.py

A tiny harness demonstrating:
- canonicalizing an input
- binding a policy version to a deterministic mapping function
- replaying the same input to get identical output
"""

from canonicalize import canonical_json, sha256_of

# Example: trivial policy mapping registry
POLICY_REGISTRY = {
    # policy_version: mapping function
    "policy_v1": lambda inp: {"outcome": "approve" if inp.get("amount", 0) < 1000 else "escalate"},
    "policy_v2": lambda inp: {"outcome": "approve" if inp.get("amount", 0) <= 500 else "escalate"},
}

def decide(input_obj, policy_version="policy_v1"):
    key = sha256_of(input_obj)
    # in a full system you'd persist the key -> decision along with policy_version
    decision = POLICY_REGISTRY[policy_version](input_obj)
    return {"key": key, "policy_version": policy_version, "decision": decision}

def replay(recorded_input, recorded_policy_version):
    # replay should give identical result
    return decide(recorded_input, recorded_policy_version)

if __name__ == "__main__":
    input1 = {"amount": 100, "reason": "refund", "metadata": {"user": "alice"}}
    rec = decide(input1, "policy_v1")
    print("Initial decision:", rec)
    rep = replay(input1, rec["policy_version"])
    print("Replay decision:", rep)
    assert rec["decision"] == rep["decision"]
