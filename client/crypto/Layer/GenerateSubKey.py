import os
import hashlib
from Crypto.Protocol.KDF import PBKDF2
import hmac


def load_binary_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
        return data
    except Exception as e:
        print(f"读取文件 {file_path} 时出现错误：{str(e)}")
        return None

def generate_sub_key(main_key, salt, key_length=32, iterations=100000):
    sub_key = PBKDF2(main_key, salt, dkLen=key_length, count=iterations, prf=lambda p, s: hmac.new(p, s, hashlib.sha256).digest())
    return sub_key
