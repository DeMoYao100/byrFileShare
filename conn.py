from enum import Enum


class ConnStatus:
    Ok = 0
    Closed = 1


class ServerConn:
    def send(self,msg: bytes) -> bool:
        return True
    def recv(self, buflen: int = 4096) -> bytes:
        return b''
    def close(self) -> None:
        pass
    def stat(self) -> ConnStatus:
        return ConnStatus()
    def recv_file(self, local_path: str) -> bool:
        return True