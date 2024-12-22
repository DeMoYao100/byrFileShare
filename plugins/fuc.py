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



