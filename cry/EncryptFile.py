# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter
import os

def load_binary_file(file_path):
    try:
        with open(file_path+'.bin', 'rb') as file:
            data = file.read()
        return data
    except Exception as e:
        print(f"读取文件 {file_path} 时出现错误：{str(e)}")
        return None
def encrypt_file(input_file, sub_key):
    try:
        # 生成随机的IV（Initialization Vector）
        iv = os.urandom(16)
        iv_int = int.from_bytes(iv, byteorder='big')
        ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)
        # 创建AES加密器，使用CTR模式
        cipher = AES.new(sub_key, AES.MODE_CTR, counter=ctr)

        if input_file is not None:
            # 加密数据
            ciphertext = cipher.encrypt(input_file)
            return ciphertext, iv

    except Exception as e:
        print(f"加密文件时出现错误：{str(e)}")
        return None
