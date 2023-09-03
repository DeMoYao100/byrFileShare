# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from Crypto.Util import Counter
import os

# 加载AES密钥
def load_aes_key(key_file):
    with open(key_file, "rb") as file:
        key = file.read()
    return key

# 使用AES解密文件
def decrypt_file(input_file, output_file, key):
    with open(input_file, "rb") as infile, open(output_file, "wb") as outfile:
        # 从输入文件中读取IV值
        iv = infile.read(16)  # IV值的长度为16字节
        ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

        while True:
            chunk = infile.read(4096)  # 逐块读取加密文件
            if not chunk:
                break
            decrypted_chunk = cipher.decrypt(chunk)
            outfile.write(decrypted_chunk)

if __name__ == "__main__":
    key_file = "sub_key.bin"  # 密钥文件
    encrypted_file = "encrypted_file.bin"  # 要解密的文件
    decrypted_file = "decrypted_file.txt"  # 解密后的文件

    key = load_aes_key(key_file)  # 加载AES密钥

    decrypt_file(encrypted_file, decrypted_file, key)
    print(f"文件 '{encrypted_file}' 已解密并保存为 '{decrypted_file}'")
