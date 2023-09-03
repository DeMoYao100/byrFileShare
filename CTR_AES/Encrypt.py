from Crypto.Cipher import AES
from Crypto.Util import Counter
import secrets
import os


# 生成128位CTR模式的AES的IV值
def generate_aes_iv():
    # 生成16字节（128位）的随机数作为IV
    iv = secrets.token_bytes(16)
    return iv


# 加载AES密钥
def load_aes_key(key_file):
    with open(key_file, "rb") as file:
        key = file.read()
    return key


# 使用AES加密文件
def encrypt_file(input_file, output_file, key):
    iv = generate_aes_iv()  # 生成IV
    ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)

    with open(input_file, "rb") as infile, open(output_file, "wb") as outfile:
        # 写入IV值到输出文件，以便解密时使用相同的IV
        outfile.write(iv)

        while True:
            chunk = infile.read(4096)  # 逐块读取文件
            if not chunk:
                break
            encrypted_chunk = cipher.encrypt(chunk)
            outfile.write(encrypted_chunk)


if __name__ == "__main__":
    key_file = "sub_key.bin"  # 密钥文件
    input_file = "plaintext.txt"  # 要加密的文件
    output_file = "encrypted_file.bin"  # 加密后的文件

    key = load_aes_key(key_file)  # 加载AES密钥

    encrypt_file(input_file, output_file, key)
    print(f"文件 '{input_file}' 已使用AES加密并保存为 '{output_file}'")
