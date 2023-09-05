import socket
from enum import Enum
from CA_verify import verify_certificate
from SignatureSystem import verify_sig
import base64
import hashlib
import json
import os

class ConnStatus(Enum):
    Ok = 0
    Closed = 1

class ServerConn:
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
        n1 = int(os.urandom(32).hex())
        self.sock.send(str(n1).encode())
        
        # 接收，n2, g^a, CA(S)的json文件
        msg = self.sock.recv(4096)
        msg = json.loads(msg.decode())
        
        # 调用验证CA的算法
        n2 = msg['n2']
        g_a = msg['g_a']
        CA = base64.b64decode(msg['CA'])
        ca_public_key_path = "ca_public_key.bin"
        with open(ca_public_key_path, 'r') as file:
            ca_public_key = file.read()
        sig_public_key = verify_certificate(CA, ca_public_key)
        b = int(os.urandom(32).hex())
        g_b = pow(g_a, b, p)
        self.sock.send(str(g_b).encode())
        
        # 接收并验证签名算法
        sig_s = self.sock.recv(4096)
        verify_sig(sig_s, sig_public_key)

        self.key = pow(g_a, b, p)
        key_bytes = self.key.to_bytes(256, byteorder='big')
        sha256 = hashlib.sha256()
        sha256.update(key_bytes)
        self.key = sha256.hexdigest()


    def send(self, msg: bytes) -> bool:
        cipher_msg = msg
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
                if e.errno == 10035:  # Resource temporarily unavailable
                    continue
                else:
                    break
            if not data:
                break
            cipher_msg += data
        self.sock.setblocking(True)
        plain_msg = cipher_msg
        return plain_msg
    
    def close(self) -> None:
        self.sock.close()
        self.status = ConnStatus.Closed

    def stat(self) -> ConnStatus:
        return self.status
    
    def recv_file(self, local_path: str) -> bool:
        with open(local_path, "wb") as f:
            try:
                data = self.sock.recv(4096)
            except:
                self.status = ConnStatus.Closed
                return False
            f.write(data)
            self.sock.setblocking(False)
            while True:
                try:
                    data = self.sock.recv(4096)
                except socket.error as e:
                    if e.errno == 10035:
                        continue
                    else:
                        break
                if not data:
                    break
                f.write(data)
        self.sock.setblocking(True)
        return True
    

if __name__ == '__main__':
    conn = ServerConn()
    # # generate authcode
    # conn.send(b'{"op": "gen-authcode", "email": "jinyi.xia@bupt.edu.cn"}')
    # print(conn.recv())
    # login in
    conn.send(b'{"op": "authcode-login", "email": "jinyi.xia@bupt.edu.cn", "authcode": "CD0875F0"}')
    print(conn.recv())
    # conn.send(b'{"op": "pwd-login", "email": "jinyi.xia@bupt.edu.cn", "pwd": "p@ssw0rd"}')
    # print(conn.recv())
    # # create dir
    # conn.send(b'{"op": "create-dir", "id": "jinyi.xia@bupt.edu.cn", "path": "./new_folder_1"}')
    # print(conn.recv())
    # conn.send(b'{"op": "create-dir", "id": "jinyi.xia@bupt.edu.cn", "path": "./new_folder_2"}')
    # print(conn.recv())
    # get dir list
    conn.send(b'{"op": "get-dir-list", "id": "jinyi.xia@bupt.edu.cn", "path": "."}')
    print(conn.recv())
    conn.close()