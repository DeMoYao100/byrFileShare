# Placeholder

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




def verify_certificate(cert, ca_public_key):
    try:
        # ��CA�Ĺ�Կ��֤֤��
        ca_public_key.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            cert.signature_hash_algorithm,
        )
        return True
    except Exception as e:
        print(f"֤����֤ʧ��: {e}")
        return False




def get_authcode(email: str) -> Optional[str]:
    """Get authcode by email

    Args:
        email (str): The email

    Returns:
        Optional[str]: The authcode if available, None otherwise
    """
    with sqlite3.connect(path) as db_conn:
        cursor = db_conn.execute(
            f'''
            SELECT *
            FROM AUTHCODE_INFO
            WHERE email = "{email}"
            '''
        )
        all = cursor.fetchall()
    if len(all) == 0:
        return None
    if all[0][2] + 600 < int(time.time()):
        del_authcode(email)
        return None
    return all[0][1]




def verify_certificate(cert, ca_public_key):
    try:
        # ��CA�Ĺ�Կ��֤֤��
        ca_public_key.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            cert.signature_hash_algorithm,
        )
        return True
    except Exception as e:
        print(f"֤����֤ʧ��: {e}")
        return False



