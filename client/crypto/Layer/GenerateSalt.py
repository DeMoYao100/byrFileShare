import secrets
import string
import os

def generate_salt(length=2):
    # 生成一个包含大小写字母和数字的字符集
    characters = string.ascii_letters + string.digits

    # 使用secrets模块生成随机的盐值
    salt = ''.join(secrets.choice(characters) for _ in range(length))
    return salt.encode()