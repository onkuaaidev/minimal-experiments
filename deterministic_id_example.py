from canonicalize import sha256_of

a = {"b": [2,1], "a": 1}
b = {"a": 1, "b": [2,1]}

print("a id:", sha256_of(a))
print("b id:", sha256_of(b))
assert sha256_of(a) == sha256_of(b)
