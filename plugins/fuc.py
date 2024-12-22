# Placeholder

def crypt_send_bytes(conn: socket.socket, key: bytes, msg: bytes):
    iv = Crypto.Random.get_random_bytes(16)
    aes = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, iv)
    cipher_msg = iv + aes.encrypt(msg)
    conn.send(cipher_msg)




    def send(self, msg: bytes) -> bool:
        iv = Crypto.Random.get_random_bytes(16)
        aes = Crypto.Cipher.AES.new(self.key, Crypto.Cipher.AES.MODE_CFB, iv)
        cipher_msg = iv + aes.encrypt(msg)
        try:
            self.sock.send(cipher_msg)
            return True
        except:
            self.status = ConnStatus.Closed
            return False
        


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


def get_file(prefix: str, full_name: str) -> Optional[bytes]:
    """Get the file list of the user's path or group's path

    Args:
        prefix (str): The email of the user or the id of the group
        full_name (str): The path of the file (including file name)

    Returns:
        bytes: The file, None if the path is invalid or the user/group does not exist
    """
    if '@' in prefix:
        path_prefix = hashlib.md5(prefix.encode()).hexdigest()
    else:
        path_prefix = prefix
    return file.get_file(os.path.join(path_prefix, full_name))




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


def handle_create_dir(conn: socket.socket, key, email: str, msg: dict):
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request create-dir')
    if services.create_dir(msg['id'], msg['path']) == model.FileOpStatus.Ok:
        crypt_send_msg(conn, key, {'status': 200})
    else:
        crypt_send_msg(conn, key, {'status': 400})




    def close(self) -> None:
        self.sock.close()
        self.status = ConnStatus.Closed



    def recv(self) -> bytes:
        try:
            cipher_msg = self.sock.recv(4096)
        except:
            self.status = ConnStatus.Closed
            return b''
        self.sock.setblocking(False)
        while True:
            try:
                data = self.sock.recv(4096)
            except socket.error as e:
                # if e.errno == 10035:  # Resource temporarily unavailable
                #     continue
                # else:
                break
            if not data:
                break
            cipher_msg += data
        self.sock.setblocking(True)
        iv = cipher_msg[:16]
        aes = Crypto.Cipher.AES.new(self.key, Crypto.Cipher.AES.MODE_CFB, iv)
        plain_msg = aes.decrypt(cipher_msg[16:])
        return plain_msg
    


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

