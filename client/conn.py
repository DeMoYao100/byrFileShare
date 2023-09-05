from enum import Enum
from flask import jsonify
import socket

class ConnStatus:
    Ok = 0
    Closed = 1


class ServerConn:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(('192.168.43.90', 2057))
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
        cipher_msg = b''
        try:
            cipher_msg = self.sock.recv(4096)
            print(cipher_msg)
        except:
            self.status = ConnStatus.Closed
            print(" except : ")
            return b''
        self.sock.setblocking(False)
        while True:
            try:
                data = self.sock.recv(4096)
                break
            except socket.error as e:
                print("lld : " ,e.errno)
                if e.errno == 10035:  # Resource temporarily unavailable
                    # continue
                    break
                else:
                    break
            if not data:
                break
            cipher_msg += data
        self.sock.setblocking(True)
        plain_msg = cipher_msg
        print("plain_msg : ", plain_msg)
        return plain_msg

    def close(self) -> None:
        self.sock.close()
        self.status = ConnStatus.Closed

    def stat(self) -> ConnStatus:
        return self.status

    def recv_file(self, local_path: str) -> bool:
        with open(local_path, "wb") as f:
            tmpdata = b' {test} '
            try:
                data = self.sock.recv(4096)
                print(" 11 : ",data)
                tmpdata = data
            except:
                self.status = ConnStatus.Closed
                return False
            f.write(tmpdata)
            self.sock.setblocking(False)
            while True:
                try:
                    data = self.sock.recv(4096)
                    tmpdata += data
                    print(" 11 : ",data)
                except socket.error as e:
                    if e.errno == 10035:
                        continue
                    else:
                        break
                if not data:
                    break
                f.write(tmpdata)
        self.sock.setblocking(True)
        return True