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
            self.sock.setblocking(False)  # 将套接字设置为非阻塞模式
            while True:
                try:
                    data = self.sock.recv(4096)
                except socket.error as e:
                    if e.errno == 10035:  # 如果是 "Resource temporarily unavailable" 错误，则继续循环
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
    conn.send(b'{"op": "login", "email": "jinyi.xia@bupt.edu.cn", "pwd": "p@ssw0rd"}')
    print(conn.recv())
    conn.send(b'{"op": "pwd-login", "email": "jinyi.xia@bupt.edu.cn", "pwd": "P@SSW0RD"}')
    print(conn.recv())
    conn.close()