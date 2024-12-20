# Placeholder

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




def update_pwd(email: str, pwdhash: str, salt: str) -> bool:
    """Update a user's password

    Args:
        email (str): The email of the user
        pwdhash (str): The new password hash
        salt (str): The new salt

    Returns:
        bool: True if the user was updated, False if the user does not exist
    """
    if get_user(email) is None:
        return False
    with sqlite3.connect(path) as db_conn:
        db_conn.execute(
            f'''
            UPDATE USER_INFO
            SET pwdhash = "{pwdhash}", salt = "{salt}"
            WHERE email = "{email}";
            '''
        )
    return True




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
    



def pwd_login_verify(email: str, pwd: str) -> bool:
    """Verify login by email and password
    
    Args:
        email (str): The email of the user
        pwd (str): The password of the user

    Returns:
        bool: True if verified, False otherwise
    """
    expected = db.get_user(email)
    if expected is None:
        return False
    return hashlib.sha256(f'{pwd}{expected.salt}'.encode()).hexdigest() == expected.pwdhash



