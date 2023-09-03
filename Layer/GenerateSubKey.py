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

def save_key_to_file(key, file_path):
    try:
        with open(file_path, 'wb') as key_file:
            key_file.write(key)
        print(f"子密钥已保存到文件 {file_path}")
    except Exception as e:
        print(f"保存子密钥到文件时出现错误：{str(e)}")

if __name__ == "__main__":
    main_key_file_path = "main_key.bin"
    salt_file_path = "salt.bin"
    sub_key_file_path = "sub_key.bin" #保存子密钥的路径

    # 读取主密钥和盐值的二进制文件
    main_key = load_binary_file(main_key_file_path)
    salt = load_binary_file(salt_file_path)

    if main_key is not None and salt is not None:
        # 生成子密钥
        sub_key = generate_sub_key(main_key, salt, key_length=32)  # 256位子密钥

        # 保存子密钥到二进制文件
        save_key_to_file(sub_key, sub_key_file_path)
