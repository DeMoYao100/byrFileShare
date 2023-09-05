import socket
from enum import Enum


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
    import secrets
    conn = ServerConn()
    # # generate authcode
    # conn.send(b'{"op": "gen-authcode", "email": "jinyi.xia@bupt.edu.cn"}')
    # print(conn.recv())
    # login in
    # conn.send(b'{"op": "authcode-login", "email": "jinyi.xia@bupt.edu.cn", "authcode": "CD0875F0"}')
    # print(conn.recv())
    conn.send(b'{"op": "pwd-login", "email": "jinyi.xia@bupt.edu.cn", "pwd": "p@ssw0rd"}')
    print(conn.recv())
    # # create dir
    # conn.send(b'{"op": "create-dir", "id": "jinyi.xia@bupt.edu.cn", "path": "./new_folder_1"}')
    # print(conn.recv())
    # conn.send(b'{"op": "create-dir", "id": "jinyi.xia@bupt.edu.cn", "path": "./new_folder_2"}')
    # print(conn.recv())
    # # put file
    # conn.send(b'{"op": "put-file", "id": "jinyi.xia@bupt.edu.cn", "path": "./hello.txt"}')
    # assert conn.recv() == b'200'
    # conn.send(b'200')
    # assert conn.recv() == b'200'
    # file = secrets.token_hex(65536).encode()
    # print(file)
    # conn.send(file)
    # print(conn.recv())
    # get dir list
    conn.send(b'{"op": "get-dir-list", "id": "jinyi.xia@bupt.edu.cn", "path": "."}')
    print(conn.recv())
    # get file
    conn.send(b'{"op": "get-file", "id": "jinyi.xia@bupt.edu.cn", "path": "./hello.txt"}')
    conn.recv_file('downloaded.txt')
    conn.close()