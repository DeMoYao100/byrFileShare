# -*- coding: utf-8 -*-
import hmac
import hashlib
import os

def load_binary_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
        return data
    except Exception as e:
        print(f"读取文件 {file_path} 时出现错误：{str(e)}")
        return None

def generate_hmac(salt, encrypted_data, key):
    try:
        # 将盐值与加密后的数据合并
        data_to_hash = salt + encrypted_data

        # 使用HMAC-SHA256散列算法生成HMAC
        hmac_value = hmac.new(key, data_to_hash, hashlib.sha256).digest()
        return hmac_value
    except Exception as e:
        print(f"生成HMAC时出现错误：{str(e)}")
        return None

if __name__ == "__main__":
    salt_file_path = "salt.bin"  # 盐值的文件路径
    encrypted_file_path = "encrypted_file.bin"  # 已加密文件的文件路径
    hmac_key = b"your_hmac_key"  # 用于生成HMAC的密钥，必须是字节串

    # 读取盐值和已加密文件的内容
    salt = load_binary_file(salt_file_path)
    encrypted_data = load_binary_file(encrypted_file_path)

    if salt is not None and encrypted_data is not None:
        # 生成HMAC
        hmac_value = generate_hmac(salt, encrypted_data, hmac_key)

        if hmac_value is not None:
            print(f"生成的HMAC：{hmac_value.hex()}")
