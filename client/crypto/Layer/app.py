# -*- coding: utf-8 -*-
from EncryptFile import load_binary_file, encrypt_file
from GenerateMainKey import generate_secure_key, generate_personal_key_id, save_key_to_usb,generate_group_key_id
from GenerateSalt import generate_salt, save_salt_to_file
from GenerateSubKey import generate_sub_key, save_key_to_file
from HMAC import generate_hmac

# 指定U盘的路径
usb_drive_path = "E:/大三上/CourseDesign/byrFileShare/Layer"  # U盘路径

# 生成安全主密钥
main_key = generate_secure_key()

user_email = input("请输入您的邮箱地址: ")

#前端选择，用于判断是否是群空间密钥
if personal:
    # 生成随机的keyID
    key_id = generate_personal_key_id(user_email)

    # 将主密钥保存到U盘，使用keyID作为文件名
    save_key_to_usb(main_key, usb_drive_path, key_id)
else if group:
    # 生成随机的keyID
    key_id = generate_group_key_id()

    # 将主密钥保存到U盘，使用keyID作为文件名
    save_key_to_usb(main_key, usb_drive_path, key_id)

salt = generate_salt()
file_path = "E:/大三上/CourseDesign/byrFileShare/Layer/salt.bin"  # 保存盐值的文件路径

# 保存盐值到二进制文件
save_salt_to_file(salt, file_path)

main_key_file_path = "main_key.bin"
salt_file_path = "salt.bin"  # 盐值的文件路径
sub_key_file_path = "sub_key.bin"  # 保存子密钥的路径

# 读取主密钥和盐值的二进制文件
main_key = load_binary_file(main_key_file_path)
salt = load_binary_file(salt_file_path)

if main_key is not None and salt is not None:
    # 生成子密钥
    sub_key = generate_sub_key(main_key, salt, key_length=32)  # 256位子密钥

    # 保存子密钥到二进制文件
    save_key_to_file(sub_key, sub_key_file_path)

input_file_path = "plaintext.txt"  # 要加密的文件
output_file_path = "encrypted_file.bin"  # 加密后的文件保存路径

# 读取子密钥
sub_key = load_binary_file(sub_key_file_path)

if sub_key is not None:
    # 加密文件
    encrypt_file(input_file_path, output_file_path, sub_key)

encrypted_file_path = "encrypted_file.bin"  # 已加密文件的文件路径
hmac_key = b"your_hmac_key"  # 用于生成HMAC的密钥，必须是字节串

# 读取盐值和已加密文件的内容
salt = load_binary_file(salt_file_path)
encrypted_data = load_binary_file(encrypted_file_path)

if salt is not None and encrypted_data is not None:
    # 生成HMAC
    hmac_value = generate_hmac(salt, encrypted_data, hmac_key)

    if hmac_value is not None:
        print(f"生成的HMAC：{hmac_value.hex()}")
