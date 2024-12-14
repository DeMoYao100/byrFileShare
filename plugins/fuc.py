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




def handle_register(conn: socket.socket, key, email: str, msg: dict) -> bool:
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request register')
    if services.register(email, msg['pwd'], msg['authcode']):
        crypt_send_msg(conn, key, {'status': 200})
        return True
    else:
        crypt_send_msg(conn, key, {'status': 400})
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




    def close(self) -> None:
        self.sock.close()
        self.status = ConnStatus.Closed



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



