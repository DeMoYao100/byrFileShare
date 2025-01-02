# Placeholder

def crypt_send_bytes(conn: socket.socket, key: bytes, msg: bytes):
    iv = Crypto.Random.get_random_bytes(16)
    aes = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, iv)
    cipher_msg = iv + aes.encrypt(msg)
    conn.send(cipher_msg)



