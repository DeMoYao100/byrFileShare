import socket
from enum import Enum
from CA_verify import verify_certificate, extract_public_key_from_certificate
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from SignatureSystem import verify_sig
import base64
import hashlib
import json
import os
from cryptography import x509
import Crypto.PublicKey.RSA
import Crypto.Cipher.PKCS1_v1_5
import Crypto.Random
import Crypto.Cipher.AES


class ConnStatus(Enum):
    Ok = 0
    Closed = 1


class ServerConn:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(('192.168.43.106', 2057))
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
        # ca_public_pem_path = "ca_public_key.pem"
        # with open(ca_public_pem_path, 'rb') as file:
        # ca_public_pem = file.read()
        ca_public_pem = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxWKWrJMRE3LBlSiSPzjX\nmnlcYHdjwHSFsimZAHpO1gwO9CG0WtDELF1h4JfkqYoEn+XiShv5L/IZcl54O/OT\nvJ4Gtu1U3Z8AkS1c9sQT8QOMD/44pT2RkioCU9+OZga8xjoNaHrTGH2qfPSke5mo\ndqlKVpCMSAIPP5FZKRPnLVoUs2fdDF9WCSiocD+cgZkbNqqyAMsPZtL40zwSgjdG\nY6V4dTphU0HS7x/KafDz32NR9E/PPvV1WC2/le56cYl3zisMeoT7BhrEVi5Pgqzs\nBiXfkbhiWelR06uM2o5NouevKq/IAt1sdiHJCKJQ+C+PjlNBh0ZHmBysFK5Z7G4F\ntQIDAQAB\n-----END PUBLIC KEY-----\n'
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

    def recv(self) -> bytes:
        try:
            cipher_msg = self.sock.recv(4096)
        except:
            self.status = ConnStatus.Closed
            return b''
        self.sock.setblocking(False)
        while True:
            try:
                data = self.sock.recv(4096)
            except socket.error as e:
                # if e.errno == 10035:  # Resource temporarily unavailable
                #     continue
                # else:
                break
            if not data:
                break
            cipher_msg += data
        self.sock.setblocking(True)
        iv = cipher_msg[:16]
        aes = Crypto.Cipher.AES.new(self.key, Crypto.Cipher.AES.MODE_CFB, iv)
        plain_msg = aes.decrypt(cipher_msg[16:])
        return plain_msg

    def close(self) -> None:
        self.sock.close()
        self.status = ConnStatus.Closed

    def stat(self) -> ConnStatus:
        return self.status
