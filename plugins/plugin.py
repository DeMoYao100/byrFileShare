# Placeholder

def handle_update_pwd(conn: socket.socket, key, email: str, msg: dict) -> bool:
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request update-pwd')
    if services.update_pwd(email, msg['pwd'], msg['authcode']):
        crypt_send_msg(conn, key, {'status': 200})
        return True
    else:
        crypt_send_msg(conn, key, {'status': 400})
        return False




def crypt_recv_bytes(conn: socket.socket, key) -> bytes:
    cipher_msg = conn.recv(4096)
    iv = cipher_msg[:16]
    aes = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, iv)
    plain_msg = aes.decrypt(cipher_msg[16:])
    return plain_msg




def load_certificate_file(file_name):
    try:
        with open(file_name, 'r') as file:
            certificate = file.read()
        return certificate
    except FileNotFoundError:
        print(f"文件 {file_name} 未找到")
        return None
    except IOError:
        print("文件读取错误")
        return None




def load_certificate_file(file_name):
    try:
        with open(file_name, 'r') as file:
            certificate = file.read()
        return certificate
    except FileNotFoundError:
        print(f"文件 {file_name} 未找到")
        return None
    except IOError:
        print("文件读取错误")
        return None




def update_pwd(email: str, pwd: str, authcode: str) -> bool:
    """Update password of a user
    
    Args:
        email (str): The email of the user
        pwd (str): The password of the user
        authcode (str): The authcode of the user

    Returns:
        bool: True if updated, False otherwise
    """
    if db.get_user(email) is None or authcode != db.get_authcode(email):
        return False
    salt = secrets.token_urlsafe(16)
    pwdhash = hashlib.sha256(f'{pwd}{salt}'.encode()).hexdigest()
    db.update_pwd(email, pwdhash, salt)
    return True




def check_group(id: str) -> bool:
    """Check if a group exists

    Args:
        id (str): The id of the group

    Returns:
        bool: True if the group exists, False otherwise
    """
    with sqlite3.connect(path) as db_conn:
        cursor = db_conn.execute(
            f'''
            SELECT *
            FROM GROUP_INFO
            WHERE id = "{id}"
            '''
        )
        all = cursor.fetchall()
    return len(all) > 0




    def close(self) -> None:
        self.sock.close()
        self.status = ConnStatus.Closed



def verify_certificate(cert, ca_public_key):
    try:
        # 用CA的公钥验证证书
        ca_public_key.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            cert.signature_hash_algorithm,
        )
        return True
    except Exception as e:
        print(f"证书验证失败: {e}")
        return False




def load_certificate_file(file_name):
    try:
        with open(file_name, 'r') as file:
            certificate = file.read()
        return certificate
    except FileNotFoundError:
        print(f"文件 {file_name} 未找到")
        return None
    except IOError:
        print("文件读取错误")
        return None




def crypt_send_msg(conn: socket.socket, key, msg: dict):
    plain_msg = json.dumps(msg).encode()
    crypt_send_bytes(conn, key, plain_msg)




def put_file(full_name: str, content: bytes) -> bool:
    """Put a file to the path

    Args:
        full_name (str): The path of the file (including file name)
        content (bytes): The content of the file

    Returns:
        bool: True if the file was put, False otherwise
    """
    path = os.path.join(storage_path, full_name)
    if os.path.exists(path):
        return False
    with open(path, 'wb') as f:
        f.write(content)
    return True




def create_dir(full_path: str) -> bool:
    """Create a directory to the path

    Args:
        full_path (str): The full path of the new directory

    Returns:
        bool: True if the directory was created, False otherwise
    """
    path = os.path.join(storage_path, full_path)
    if os.path.exists(path):
        return False
    os.mkdir(path)
    return True




def load_certificate_file(file_name):
    try:
        with open(file_name, 'r') as file:
            certificate = file.read()
        return certificate
    except FileNotFoundError:
        print(f"文件 {file_name} 未找到")
        return None
    except IOError:
        print("文件读取错误")
        return None



