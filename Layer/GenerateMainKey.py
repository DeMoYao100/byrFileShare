import os
import secrets
import hashlib

def generate_personal_key_id(email):
    # 计算用户输入的邮箱的MD5哈希值
    email_md5 = hashlib.md5(email.encode()).hexdigest()
    return email_md5

def generate_group_key_id():
    # 生成128位（16字节）的随机数作为keyID
    group_key_id = secrets.token_hex(16)
    return group_key_id

def generate_secure_key():
    # 生成256位（32字节）的安全主密钥
    secure_key = secrets.token_bytes(32)
    return secure_key

def save_key_to_usb(key, usb_drive_path, key_id):
    # 使用keyID作为文件名将密钥保存为二进制文件
    key_file_name = f"{key_id}.bin"
    key_file_path = os.path.join(usb_drive_path, key_file_name)

    try:
        with open(key_file_path, "wb") as key_file:
            key_file.write(key)
        print(f"主密钥已保存到U盘 {usb_drive_path} 中的 {key_file_name} 文件")
    except Exception as e:
        print(f"保存主密钥到U盘时出现错误：{str(e)}")