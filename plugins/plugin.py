# Placeholder

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
        
        # 接收，n2, g^a, CA(S)的json文件
        msg = self.sock.recv(4096)
        msg = json.loads(msg.decode())
        
        # 调用验证CA的算法
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

        # 接收并验证签名算法
        sig_s = self.sock.recv(4096)
        verify_sig(sig_s, n1, n2, g_a, g_b, sig_public_key)
 
        self.key = pow(g_a, b, p)
        key_bytes = self.key.to_bytes(256, byteorder='big')
        sha256 = hashlib.sha256()
        sha256.update(key_bytes)
        self.key = sha256.digest()



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




def check_path(full_path: str) -> bool:
    """Check if the path exists

    Args:
        full_path (str): The path to check

    Returns:
        bool: True if the path is valid, False otherwise
    """
    path = os.path.join(storage_path, full_path)
    return os.path.exists(path)




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



