from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def get_sig(n1, n2, g_a, g_b, private_key):
    message = f"{n1},{n2},{g_a},{g_b}"
    hash_obj = SHA256.new(message.encode('utf-8'))
    signer = pkcs1_15.new(RSA.import_key(private_key))
    return signer.sign(hash_obj)

def verify_sig(sig_s, public_key):
    hash_obj = SHA256.new(sig_s)
    verifier = pkcs1_15.new(RSA.import_key(public_key.encode('utf-8')))

    try:
        verifier.verify(hash_obj, sig_s)
        print("Signature is valid.")
    except (ValueError, TypeError):
        print("Signature is invalid.")