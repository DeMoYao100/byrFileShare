# -*- coding: utf-8 -*-
from EncryptFile import load_binary_file, encrypt_file
from GenerateSalt import generate_salt
from GenerateSubKey import generate_sub_key
from HMAC import generate_hmac
from GenerateMainKey import generate_group_key_id

def layer_encrypt(input_file, keyID):
    # 指定U盘的路径
    usb_drive_path = "E:/大三上/CourseDesign/byrFileShare/Layer"  # U盘路径
    '''
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
    '''
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
            return salt + keyID.encode('utf-8') + encrypted_file + iv + hmac_value
    return None