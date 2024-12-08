
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



