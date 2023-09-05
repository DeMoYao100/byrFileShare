from enum import Enum
from flask import jsonify

class ConnStatus:
    Ok = 0
    Closed = 1


class ServerConn:
    def send(self,msg: bytes) -> bool:
        return True
    def recv(self, buflen: int = 4096) -> bytes:
        return jsonify({'status':200}).get_data()
    def close(self) -> None:
        pass
    def stat(self) -> ConnStatus:
        return ConnStatus()
    def recv_file(self, local_path: str) -> bool:
        return True