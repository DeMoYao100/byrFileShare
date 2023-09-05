```
from Crypto.PublicKey import RSA

key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

```

```
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

n1 = 123
n2 = 456
g_a = 789
g_b = 101112

message = f"{n1},{n2},{g_a},{g_b}"

hash_obj = SHA256.new(message.encode('utf-8'))
signer = pkcs1_15.new(RSA.import_key(private_key))
signature = signer.sign(hash_obj)

```

```
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

hash_obj = SHA256.new(message.encode('utf-8'))
verifier = pkcs1_15.new(RSA.import_key(public_key))

try:
    verifier.verify(hash_obj, signature)
    print("Signature is valid.")
except (ValueError, TypeError):
    print("Signature is invalid.")

```

