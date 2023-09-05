import hashlib
import hmac

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


def extract_values_from_encrypted_file(file_stream):
    salt = file_stream[:16]
    keyID = file_stream[2:2 + 16]
    cipher_data = file_stream[2 + 16:-32-2-1]
    iv = file_stream[-32 - 2 - 1:-32 - 1]
    hmac = file_stream[-32:]
    print(salt, keyID, cipher_data, iv, hmac)
    return salt, keyID, cipher_data, iv, hmac


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


def layer_decrypt(cipher_file):
    salt, keyID, cipher_data, iv, hmac = extract_values_from_encrypted_file(cipher_file)
    usb_drive_path = "E:/大三上/CourseDesign/byrFileShare/Layer"
    main_key_file_path = keyID.decode('utf-8') + '.bin'
    main_key = load_binary_file(main_key_file_path)

    if main_key is not None and salt is not None:
        sub_key = generate_sub_key(main_key, salt, key_length=32)  # 256位子密钥
        cipher = AES.new(sub_key, AES.MODE_CTR, nonce=iv)
        decrypted_data = cipher.decrypt(cipher_data)
        return decrypted_data

    else:
        print("main key 和 salt 读取错误")
        return None
if __name__ == '__main__':
    cipher_file = load_binary_file('cipher.bin')
    plain_file = layer_decrypt(cipher_file)
    print(plain_file)



