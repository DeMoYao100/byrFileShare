# -*- coding: utf-8 -*-
import os

from cry.EncryptFile import load_binary_file, encrypt_file
from cry.GenerateSalt import generate_salt
from cry.GenerateSubKey import generate_sub_key
from cry.HMAC import generate_hmac
from cry.GenerateMainKey import save_key_to_usb, generate_secure_key, generate_group_key_id


def layer_encrypt(input_file, keyID):
    # 指定U盘的路径
    usb_drive_path = "O:"  # U盘路径

    if input_file is not None:
        salt = generate_salt()

        main_key_file_path = keyID
        # 读取主密钥和盐值的二进制文件
        main_key = load_binary_file(main_key_file_path)

        sub_key = None

        if main_key is not None and salt is not None:
            sub_key = generate_sub_key(main_key, salt, key_length=32)  # 256位子密钥

        encrypted_file = None
        iv = None

        if sub_key is not None:
            # 加密文件
            encrypted_file, iv = encrypt_file(input_file, sub_key)
        hmac_key = b"your_hmac_key"  # 用于生成HMAC的密钥，必须是字节串

        if salt is not None and encrypted_file is not None:
            # 生成HMAC
            hmac_value = generate_hmac(salt, encrypted_file, hmac_key)
            if hmac_value is not None:
                #print("LayerDecrtpt", salt, "\n", keyID, "\n", encrypted_file, "\n", iv, "\n", hmac_value)
                return salt + keyID.encode('utf-8') + encrypted_file + iv + hmac_value
        return None

    else:
        main_key = generate_secure_key()
        save_key_to_usb(main_key, usb_drive_path, keyID)


def save_main_key(main_key, keyID):
    usb_drive_path = "O:"  # U盘路径
    # 使用keyID作为文件名将密钥保存为二进制文件
    key_file_name = f"{keyID}.bin"
    key_file_path = os.path.join("O:", key_file_name)

    try:
        with open(key_file_path, "wb") as key_file:
            key_file.write(main_key)
        print(f"主密钥已保存到U盘 {usb_drive_path} 中的 {key_file_name} 文件")
    except Exception as e:
        print(f"保存主密钥到U盘时出现错误：{str(e)}")


