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
    
def iv_to_hmac_key(iv: bytes, key: bytes) -> bytes:
    """
    Generate an HMAC key using the given initialization vector (iv) and key.
    :param iv: The initialization vector, must be 128 bits (16 bytes) long.
    :param key: The key to use for the HMAC algorithm.
    :return: The generated HMAC key.
    """
    if len(iv) != 16:
        raise ValueError("Initialization vector must be 128 bits (16 bytes) long")
    return hmac.new(key, iv, hashlib.sha256).digest()

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

def verify_hmac(salt, encrypted_data, key, hmac_to_check):
    try:
        # 将盐值与加密后的数据合并
        data_to_hash = salt + encrypted_data

        # 使用HMAC-SHA256散列算法生成HMAC
        computed_hmac = hmac.new(key, data_to_hash, hashlib.sha256).digest()

        # 将生成的HMAC与传入的HMAC进行比较
        if hmac.compare_digest(computed_hmac, hmac_to_check):
            print("HMAC验证成功")
        else:
            print("HMAC验证失败")
    except Exception as e:
        print(f"验证HMAC时出现错误：{str(e)}")