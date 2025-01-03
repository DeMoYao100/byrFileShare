import hashlib
import hmac

from Crypto.Cipher import AES

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad
from Crypto.Util import Counter
from cry.HMAC import verify_hmac, iv_to_hmac_key

# 从加密文件中提取值
def extract_values_from_encrypted_file(file_path):
    with open(file_path, 'rb') as file_stream:
        file_data = file_stream.read()
        salt = file_data[:2]
        keyID = file_data[2:2+32]
        cipher_data = file_data[2+32:-32-16]
        iv = file_data[-32-16:-32]
        hmac = file_data[-32:]
    #print("LayerDecrtpt", salt, "\n", keyID, "\n", cipher_data, "\n", iv, "\n", hmac)
    return salt, keyID, cipher_data, iv, hmac

# 从文件加载二进制数据
def load_binary_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
        return data
    except Exception as e:
        print(f"读取文件 {file_path} 时出现错误：{str(e)}")
        return None

# 使用PBKDF2生成子密钥
def generate_sub_key(main_key, salt, key_length=32, iterations=100000):
    sub_key = PBKDF2(main_key, salt, dkLen=key_length, count=iterations, prf=lambda p, s: hmac.new(p, s, hashlib.sha256).digest())
    return sub_key

# 使用AES-CTR模式解密数据
def layer_decrypt(cipher_file):
    # 从加密文件中提取盐（salt）、密钥ID（keyID）、密文数据（cipher_data）、初始化向量（iv）和HMAC
    salt, keyID, cipher_data, iv, hmac = extract_values_from_encrypted_file(cipher_file)
    # 验证HMAC以确保数据完整性
    verify_hmac(salt, cipher_data, iv_to_hmac_key(iv, b'secret_key'), hmac)
    usb_drive_path = "O:/"
    main_key_file_path = usb_drive_path.encode()+keyID + b'.bin'
    print("main_key_file_path:",main_key_file_path,'\n\n\n')
    # 使用keyID构建主密钥文件的路径
    main_key = load_binary_file(main_key_file_path)

    if main_key is not None and salt is not None:
        # 生成用于AES解密的子密钥
        sub_key = generate_sub_key(main_key, salt, key_length=32)  # 256位子密钥
        iv_int = int.from_bytes(iv, byteorder='big')
        # 创建AES-CTR模式的计数器，初始值为IV
        ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)
        cipher = AES.new(sub_key, AES.MODE_CTR, counter=ctr)
        # 解密密文数据
        decrypted_data = cipher.decrypt(cipher_data)
        return decrypted_data

    else:
        print("main key 和 salt 读取错误")
        return None


