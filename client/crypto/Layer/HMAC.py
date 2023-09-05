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