# Placeholder

def init(db_path: str = path) -> None:
    """Initialize the sqlite database"""
    path = db_path
    if os.path.exists(path):
        with sqlite3.connect(path) as db_conn:
            db_conn.execute('DELETE FROM AUTHCODE_INFO;')
        return
    with sqlite3.connect(path) as db_conn:
        db_conn.execute(
            '''
            CREATE TABLE USER_INFO (
                email TEXT PRIMARY KEY,
                pwdhash TEXT NOT NULL,
                salt TEXT NOT NULL
            );
            '''
        )
        db_conn.execute(
            '''
            CREATE UNIQUE INDEX USER_email ON USER_INFO (email);
            '''
        )
        db_conn.execute(
            '''
            CREATE TABLE GROUP_INFO (
                id TEXT NOT NULL,
                member TEXT NOT NULL,
                PRIMARY KEY (id, member),
                FOREIGN KEY (member) REFERENCES USER_INFO (email) ON DELETE CASCADE
            );
            '''
        )
        db_conn.execute(
            '''
            CREATE INDEX GROUP_id ON GROUP_INFO (member);
            '''
        )
        db_conn.execute(
            '''
            CREATE TABLE AUTHCODE_INFO (
                email TEXT PRIMARY KEY,
                authcode TEXT NOT NULL,
                timestamp INTEGER NOT NULL
            );
            '''
        )




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




def handle_put_file(conn: socket.socket, key, email: str, msg: dict):
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request put-file')
    if services.check_path(msg['id'], msg['path']):
        crypt_send_bytes(conn, key, b'400')
        return
    else:
        crypt_send_bytes(conn, key, b'200')
    if crypt_recv_bytes(conn, key) == b'200':
        crypt_send_bytes(conn, key, b'200')
    else:
        crypt_send_bytes(conn, key, b'400')
        return
    fifo_path = f'./tmp/{int(time.time())}.pipe'
    receive_file(fifo_path, conn)
    with open(fifo_path, 'rb') as f:
        cipher_msg = f.read()
    iv = cipher_msg[:16]
    aes = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, iv)
    plain_msg = aes.decrypt(cipher_msg[16:])
    services.put_file(msg['id'], msg['path'], plain_msg)
    crypt_send_msg(conn, key, {'status': 200})




def handle_create_dir(conn: socket.socket, key, email: str, msg: dict):
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request create-dir')
    if services.create_dir(msg['id'], msg['path']) == model.FileOpStatus.Ok:
        crypt_send_msg(conn, key, {'status': 200})
    else:
        crypt_send_msg(conn, key, {'status': 400})




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



