import os
import secrets


def generate_secure_key():
    # 生成256位（32字节）的安全主密钥
    secure_key = secrets.token_bytes(32)
    return secure_key


def save_key_to_usb(key, usb_drive_path):
    # 将密钥保存为二进制文件
    key_file_path = os.path.join(usb_drive_path, "main_key.bin")

    try:
        with open(key_file_path, "wb") as key_file:
            key_file.write(key)
        print(f"主密钥已保存到U盘 {usb_drive_path} 中的 main_key.bin 文件")
    except Exception as e:
        print(f"保存主密钥到U盘时出现错误：{str(e)}")


if __name__ == "__main__":
    # 指定U盘的路径
    usb_drive_path = "E:/大三上/CourseDesign/byrFileShare/Layer"  # U盘路径

    # 生成安全主密钥
    main_key = generate_secure_key()

    # 将主密钥保存到U盘
    save_key_to_usb(main_key, usb_drive_path)
