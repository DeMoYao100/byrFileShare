# Placeholder

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




def handle_del_dir(conn: socket.socket, key, email: str, msg: dict):
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request del-dir')
    if services.del_dir(msg['id'], msg['path']) == model.FileOpStatus.Ok:
        crypt_send_msg(conn, key, {'status': 200})
    else:
        crypt_send_msg(conn, key, {'status': 400})




def crypt_send_msg(conn: socket.socket, key, msg: dict):
    plain_msg = json.dumps(msg).encode()
    crypt_send_bytes(conn, key, plain_msg)




def handle_register(conn: socket.socket, key, email: str, msg: dict) -> bool:
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request register')
    if services.register(email, msg['pwd'], msg['authcode']):
        crypt_send_msg(conn, key, {'status': 200})
        return True
    else:
        crypt_send_msg(conn, key, {'status': 400})
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



