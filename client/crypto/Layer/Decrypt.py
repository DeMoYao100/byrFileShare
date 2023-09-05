import hashlib

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def load_binary_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
        return data
    except Exception as e:
        print(f"读取文件 {file_path} 时出现错误：{str(e)}")
        return None


def extract_values_from_encrypted_file(file_path):
    salt = None
    key_id = None
    hmac = None
    iv = None

    with open(file_path, 'rb') as file:
        # 读取前16位作为盐值
        salt = file.read(16)

        # 读取接着的128位作为keyID
        key_id = file.read(16)

        # 移动文件指针到最后256位
        file.seek(-256, 2)

        # 读取后256位作为HMAC
        hmac = file.read(32)

        # 读取前128位作为iv值
        iv = file.read(16)

    return salt, key_id, hmac, iv


def generate_sub_key(main_key, salt, key_length=32, iterations=100000):
    sub_key = PBKDF2(main_key, salt, dkLen=key_length, count=iterations,
                     prf=lambda p, s: hmac.new(p, s, hashlib.sha256).digest())
    return sub_key


def get_sub_key():
    key_id = extract_values_from_encrypted_file(file_path)
    main_key_file_path = f"{key_id}.bin"
    main_key = load_binary_file(main_key_file_path)
    salt = extract_values_from_encrypted_file(file_path)

    if main_key is not None and salt is not None:
        # 生成子密钥
        sub_key = generate_sub_key(main_key, salt, key_length=32)  # 256位子密钥
        return sub_key

def decrypt_file_with_iv(file_path, subkey, iv):
    cipher = Cipher(algorithms.AES(subkey), modes.CTR(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = b''

    with open(file_path, 'rb') as file:
        # 移动文件指针到从第272位开始（16位盐值 + 128位KeyID）

        # 逐块解密数据并追加到decrypted_data中
        while True:
            chunk = file.read(16)
            if not chunk:
                break
            decrypted_chunk = decryptor.update(chunk)
            decrypted_data += decrypted_chunk

    return decrypted_data
