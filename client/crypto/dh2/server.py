# -*- coding: utf-8 -*-
import socket
import random
import hashlib
import hmac

# Diffie-Hellman参数
p = 23  # 大素数
g = 5   # 原根

# 生成服务器私钥a
a = random.randint(1, p - 1)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12345))
    server_socket.listen(1)

    print("等待客户端连接...")
    client_socket, client_address = server_socket.accept()
    print("客户端已连接：", client_address)

    # 服务器生成n2和g^a，发送给客户端
    n2 = random.randint(1, 1000)
    ga = (g ** a) % p
    client_socket.send(f"{n2},{ga}".encode())

    # 接收客户端发送的n1，CA(Server)，g^b，和Sig_c(g^a, g^b, n1, n2)
    data = client_socket.recv(1024).decode()
    n1, ca_server, gb, sig_c = map(int, data.split(','))

    # 验证CA(Server)
    if verify_ca(ca_server):
        print("CA(Server)验证成功")
        # 计算共享密钥g^(ab)
        gab = (gb ** a) % p

        # 计算并发送Sig_s(g^a, g^b, n1, n2)
        sig_s = sign_message(ga, gb, n1, n2, gab)
        client_socket.send(str(sig_s).encode())
        print("已发送Sig_s(g^a, g^b, n1, n2)给客户端")

        # 计算会话密钥g^(ab)
        session_key = hashlib.sha256(str(gab).encode()).hexdigest()
        print("会话密钥：", session_key)

        # 在这里可以开始使用会话密钥进行加密通信

    else:
        print("CA(Server)验证失败")

    client_socket.close()
    server_socket.close()

def verify_ca(ca):
    # 这里可以实现CA验证逻辑
    return True  # 简单示例，始终返回True

def sign_message(ga, gb, n1, n2, gab):
    # 使用hmac实现数字签名
    key = str(gab).encode()
    data = f"{ga},{gb},{n1},{n2}".encode()
    return hmac.new(key, data, hashlib.sha256).hexdigest()

if __name__ == "__main__":
    main()
