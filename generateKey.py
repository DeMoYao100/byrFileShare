from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util import Counter
import os

password = b"user_password"
salt = os.urandom(16)

key = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=None)

nonce = os.urandom(8)
ctr = Counter.new(64, prefix=nonce)

cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
key_sequence = cipher.encrypt(b"\x00" * 2500)

key_list = [byte for byte in key_sequence]

print(key_list)