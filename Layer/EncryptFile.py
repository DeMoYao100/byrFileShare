# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

def load_binary_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
        return data
    except Exception as e:
        print(f"读取文件 {file_path} 时出现错误：{str(e)}")
        return None

def save_binary_file(data, file_path):
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
        print(f"数据已保存到文件 {file_path}")
    except Exception as e:
        print(f"保存数据到文件时出现错误：{str(e)}")

def encrypt_file(input_file_path, output_file_path, sub_key):
    try:
        # 生成随机的IV（Initialization Vector）
        iv = os.urandom(8)

        # 创建AES加密器，使用CTR模式
        cipher = AES.new(sub_key, AES.MODE_CTR, initial_value=iv)

        # 读取要加密的文件内容
        plaintext = load_binary_file(input_file_path)

        if plaintext is not None:
            # 加密数据
            ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

            # 将IV和加密后的数据保存到输出文件
            save_binary_file(iv + ciphertext, output_file_path)
    except Exception as e:
        print(f"加密文件时出现错误：{str(e)}")

if __name__ == "__main__":
    sub_key_file_path = "sub_key.bin"  # 子密钥的文件路径
    input_file_path = "plaintext.txt"  # 要加密的文件
    output_file_path = "encrypted_file.bin"  # 加密后的文件保存路径

    # 读取子密钥
    sub_key = load_binary_file(sub_key_file_path)

    if sub_key is not None:
        # 加密文件
        encrypt_file(input_file_path, output_file_path, sub_key)
