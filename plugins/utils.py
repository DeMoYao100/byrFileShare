# Placeholder

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




def get_dir_list(full_path: str) -> Optional[list[dict]]:
    """Get the directory list

    Args:
        full_path (str): The path of the directory

    Returns:
        list: The directory list, None if the path is invalid
    """
    path = os.path.join(storage_path, full_path)
    if not os.path.isdir(path):
        return None
    dirs = os.listdir(path)
    retval = []
    for dir in dirs:
        dir_path = os.path.join(path, dir)
        dir_dict = {'name': dir, 'type': 'file', 'size': 0, 'time': 0}


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


def get_file(full_name: str) -> Optional[bytes]:
    """Get the file

    Args:
        full_name (str): The path of the file (including file name)

    Returns:
        list: The file, None if the path is invalid
    """
    path = os.path.join(storage_path, full_name)
    if not os.path.isfile(path):
        return None
    with open(path, 'rb') as f:
        return f.read()
    



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




def recv_long(conn: socket.socket) -> bytes:
    msg = conn.recv(4096)
    conn.setblocking(False)
    while True:
        try:
            data = conn.recv(4096)
        except socket.error as e:
            # if e.errno == 10035:  # Resource temporarily unavailable
            #     continue
            # else:
            break
        if not data:
            break
        msg += data
    conn.setblocking(True)
    return msg




def add_group_user(id: str, email: str) -> bool:
    """Add a user to a group

    Args:
        id (str): The id of the group
        email (str): The email of the user

    Returns:
        bool: True if the user was added, False if the user has already been in the group
    """
    with sqlite3.connect(path) as db_conn:
        try:
            db_conn.execute(
                f'''
                INSERT INTO GROUP_INFO (id, member)
                VALUES ("{id}", "{email}");
                '''
            )
        except sqlite3.IntegrityError:
            return False
    return True




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




def crypt_recv_msg(conn: socket.socket, key) -> dict:
    plain_msg = crypt_recv_bytes(conn, key)
    return json.loads(plain_msg.decode())




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


def update_authcode(email: str, authcode: str) -> None:
    """Update authcode by email

    Args:
        email (str): The email
        authcode (str): The authcode
    """
    with sqlite3.connect(path) as db_conn:
        db_conn.execute(
            f'''
            INSERT INTO AUTHCODE_INFO (email, authcode, timestamp)
            VALUES ("{email}", "{authcode}", {int(time.time())})
            ON CONFLICT(email) DO UPDATE
            SET authcode = "{authcode}", timestamp = {int(time.time())};
            '''
        )



