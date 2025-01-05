# Placeholder

    def close(self) -> None:
        self.sock.close()
        self.status = ConnStatus.Closed



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



