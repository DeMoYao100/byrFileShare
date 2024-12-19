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



