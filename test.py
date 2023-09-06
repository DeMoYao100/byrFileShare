#
# import socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('0.0.0.0', 2057))
# s.listen(100000)
# conn, addr = s.accept()
# print (conn.recv().decode())
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.43.41',2057))
s.send(b"shellcode\x00\x00")