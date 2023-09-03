import secrets
import string
import os


def generate_salt(length=16):
    # 生成一个包含大小写字母和数字的字符集
    characters = string.ascii_letters + string.digits

    # 使用secrets模块生成随机的盐值
    salt = ''.join(secrets.choice(characters) for _ in range(length))
    return salt


def save_salt_to_file(salt, file_path):
    try:
        # 将盐值编码为字节
        salt_bytes = salt.encode('utf-8')

        # 将盐值写入二进制文件
        with open(file_path, 'wb') as salt_file:
            salt_file.write(salt_bytes)

        print(f"盐值已保存到文件 {file_path}")
    except Exception as e:
        print(f"保存盐值到文件时出现错误：{str(e)}")


if __name__ == "__main__":
    salt = generate_salt()
    file_path = "E:/大三上/CourseDesign/byrFileShare/Layer/salt.bin"  # 保存盐值的文件路径

    # 保存盐值到二进制文件
    save_salt_to_file(salt, file_path)
