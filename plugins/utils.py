# Placeholder

def crypt_send_bytes(conn: socket.socket, key: bytes, msg: bytes):
    iv = Crypto.Random.get_random_bytes(16)
    aes = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, iv)
    cipher_msg = iv + aes.encrypt(msg)
    conn.send(cipher_msg)




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



