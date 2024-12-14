# Placeholder

def put_file(prefix: str, full_name: str, content: bytes) -> FileOpStatus:
    """Put a file to the user's path or group's path

    Args:
        prefix (str): The email of the user or the id of the group
        full_name (str): The path of the file (including file name)
        content (bytes): The content of the file

    Returns:
        FileOpStatus: The status of the operation
    """
    if '@' in prefix:
        path_prefix = hashlib.md5(prefix.encode()).hexdigest()
    else:
        path_prefix = prefix
    full_path = os.path.join(path_prefix, full_name)
    if not file.put_file(full_path, content):
        return FileOpStatus.Collision
    return FileOpStatus.Ok




def del_dir(prefix: str, full_path: str) -> FileOpStatus:
    """Delete a directory and all files in it (or a single file) to the user's path or group's path

    Args:
        prefix (str): The email of the user or the id of the group
        full_path (str): The full path of the directory

    Returns:
        FileOpStatus: The status of the operation
    """
    if '@' in prefix:
        path_prefix = hashlib.md5(prefix.encode()).hexdigest()
    else:
        path_prefix = prefix
    full_path = os.path.join(path_prefix, full_path)
    if not file.del_dir(full_path):
        return FileOpStatus.PathErr
    return FileOpStatus.Ok




def get_sig(n1, n2, g_a, g_b, private_key):
    data_to_sign = f"{n1},{n2},{g_a},{g_b}"
    signature = private_key.sign(
        data_to_sign.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature




def receive_file(filename, sock):
    with open(filename, "wb") as f:
        data = sock.recv(4096)
        f.write(data)
        sock.setblocking(False)  # 将套接字设置为非阻塞模式
        while True:
            try:
                data = sock.recv(4096)
            except socket.error as e:
                # if e.errno == 10035:  # 如果是 "Resource temporarily unavailable" 错误，则继续循环
                #     continue
                # else:
                break
            if not data:
                break
            f.write(data)
    sock.setblocking(True)




def del_dir(prefix: str, full_path: str) -> FileOpStatus:
    """Delete a directory and all files in it (or a single file) to the user's path or group's path

    Args:
        prefix (str): The email of the user or the id of the group
        full_path (str): The full path of the directory

    Returns:
        FileOpStatus: The status of the operation
    """
    if '@' in prefix:
        path_prefix = hashlib.md5(prefix.encode()).hexdigest()
    else:
        path_prefix = prefix
    full_path = os.path.join(path_prefix, full_path)
    if not file.del_dir(full_path):
        return FileOpStatus.PathErr
    return FileOpStatus.Ok




def get_dir_list(prefix: str, path: str) -> Optional[list[dict]]:
    """Get the directory list of the user's path or group's path

    Args:
        prefix (str): The email of the user or the id of the group
        path (str): The path of the directory

    Returns:
        list[dict]: A list of folders and files, None if the path is invalid or the user/group does not exist

    Example:
        [{'name': 'storage', 'type': 'dir', 'size': None, 'time': 1693707480}, {'name': 'README_server.md', 'type': 'file', 'size': 14, 'time': 1693567086}, {'name': '.gitignore', 'type': 'file', 'size': 3102, 'time': 1693642614}, {'name': 'cloud_storage.db', 'type': 'file', 'size': 36864, 'time': 1693707480}, {'name': 'service', 'type': 'dir', 'size': None, 'time': 1693707150}, {'name': '.git', 'type': 'dir', 'size': None, 'time': 1693717191}, {'name': '.vscode', 'type': 'dir', 'size': None, 'time': 1693568276}]
    """
    if '@' in prefix:
        path_prefix = hashlib.md5(prefix.encode()).hexdigest()
    else:
        path_prefix = prefix
    return file.get_dir_list(os.path.join(path_prefix, path))




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




def handle_register(conn: socket.socket, key, email: str, msg: dict) -> bool:
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request register')
    if services.register(email, msg['pwd'], msg['authcode']):
        crypt_send_msg(conn, key, {'status': 200})
        return True
    else:
        crypt_send_msg(conn, key, {'status': 400})
        return False




def get_groups(email: str) -> list[str]:
    """Get a list of groups ids that a user is a member of

    Args:
        email (str): The email of the user

    Returns:
        list[str]: A list of group ids
    """
    with sqlite3.connect(path) as db_conn:
        cursor = db_conn.execute(
            f'''
            SELECT id
            FROM GROUP_INFO
            WHERE member = "{email}"
            '''
        )
        all = cursor.fetchall()
    return [g[0] for g in all]




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




    def __init__(self, email: Optional[str] = None, pwdhash: Optional[str] = None, salt: Optional[str] = None):
        """User object

        Args:
            email (Optional[str], optional): User's email. Defaults to None.
            pwdhash (Optional[str], optional): Hashcode of the user's password. Defaults to None.
            salt (Optional[str], optional): Salt of the hashcode. Defaults to None.
        """
        self.email = email
        self.pwdhash = pwdhash
        self.salt = salt


class Group:

