
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




    def close(self) -> None:
        self.sock.close()
        self.status = ConnStatus.Closed



def gen_authcode(email: str) -> bool:
    """Generate authcode by email
    
    Args:
        email (str): The email of the user

    Returns:
        bool: True if the authcode was sent, False otherwise
    """
    authcode = secrets.token_hex(4).upper()
    if _send_mail(email, authcode):
        db.update_authcode(email, authcode)
        return True
    return False




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


def load_certificate_file(file_name):
    try:
        with open(file_name, 'r') as file:
            certificate = file.read()
        return certificate
    except FileNotFoundError:
        print(f"�ļ� {file_name} δ�ҵ�")
        return None
    except IOError:
        print("�ļ���ȡ����")
        return None




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




def crypt_recv_bytes(conn: socket.socket, key) -> bytes:
    cipher_msg = conn.recv(4096)
    iv = cipher_msg[:16]
    aes = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, iv)
    plain_msg = aes.decrypt(cipher_msg[16:])
    return plain_msg




    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(('127.0.0.1', 2057))
            self.status = ConnStatus.Ok
        except:
            self.status = ConnStatus.Closed
        self.key = None

        p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
        g = 2
        n1 = int(os.urandom(32).hex(), 16)
        self.sock.send(str(n1).encode())
        
        # ���գ�n2, g^a, CA(S)��json�ļ�
        msg = self.sock.recv(4096)
        msg = json.loads(msg.decode())
        
        # ������֤CA���㷨
        n2 = msg['n2']
        g_a = msg['g_a']
        CA = base64.b64decode(msg['CA'])
        CA = x509.load_pem_x509_certificate(CA, default_backend())
        ca_public_pem_path = "ca_public_key.pem"
        with open(ca_public_pem_path, 'rb') as file:
            ca_public_pem = file.read()
        ca_public_pem = ca_public_pem
        ca_public_key = serialization.load_pem_public_key(ca_public_pem, backend=default_backend())
        pem_public = None
        if verify_certificate(CA, ca_public_key):
            pem_public = extract_public_key_from_certificate(CA)
        sig_public_key = serialization.load_pem_public_key(pem_public, backend=default_backend())
        b = int(os.urandom(32).hex(), 16)
        g_b = pow(g, b, p)
        self.sock.send(str(g_b).encode())

        # ���ղ���֤ǩ���㷨
        sig_s = self.sock.recv(4096)
        verify_sig(sig_s, n1, n2, g_a, g_b, sig_public_key)
 
        self.key = pow(g_a, b, p)
        key_bytes = self.key.to_bytes(256, byteorder='big')
        sha256 = hashlib.sha256()
        sha256.update(key_bytes)
        self.key = sha256.digest()



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




    def close(self) -> None:
        self.sock.close()
        self.status = ConnStatus.Closed



def add_user(email: str, pwdhash: str, salt: str) -> None:
    """Add a user to the database

    Args:
        email (str): The email of the user
        pwdhash (str): The password hash of the user
        salt (str): The salt of the password hash
    """
    with sqlite3.connect(path) as db_conn:
        db_conn.execute(
            f'''
            INSERT INTO USER_INFO (email, pwdhash, salt)
            VALUES ("{email}", "{pwdhash}", "{salt}");
            '''
        )




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


def check_path(prefix: str, full_path: str) -> bool:
    """Check if the directory exists

    Args:
        prefix (str): The email of the user or the id of the group
        full_path (str): The full path of the directory

    Returns:
        bool: True if exists, False otherwise
    """
    if '@' in prefix:
        path_prefix = hashlib.md5(prefix.encode()).hexdigest()
    else:
        path_prefix = prefix
    full_path = os.path.join(path_prefix, full_path)
    return file.check_path(full_path)



