# -*- coding: utf-8 -*-
import socket
import random
import hashlib
import hmac

# Diffie-Hellman参数
p = 23  # 大素数
g = 5   # 原根

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 12345))

    # 客户端生成n1和g^b
    n1 = random.randint(1, 1000)
    b = random.randint(1, p - 1)
    gb = (g ** b) % p
    client_socket.send(f"{n1},{gb}".encode())

    # 接收服务器发送的n2和g^a
    data = client_socket.recv(1024).decode()
    n2, ga = map(int, data.split(','))

    # 生成CA(Client)和Sig_c(g^a, g^b, n1, n2)
    ca_client = generate_ca()
    sig_c = sign_message(ga, gb, n1, n2, ca_client)

    # 发送CA(Client)和Sig_c(g^a, g^b, n1, n2)给服务器
    client_socket.send(f"{ca_client},{sig_c}".encode())

    # 接收服务器发送的Sig_s(g^a, g^b, n1, n2)
    sig_s = client_socket.recv(1024).decode()

    # 验证Sig_s
    if verify_signature(ga, gb, n1, n2, sig_s):
        print("Sig_s验证成功")

        # 计算共享密钥g^(ab)
        gab = (ga ** b) % p
        session_key = hashlib.sha256(str(gab).encode()).hexdigest()
        print("会话密钥：", session_key)

        # 在这里可以开始使用会话密钥进行加密通信

    else:
        print("Sig_s验证失败")

    client_socket.close()

def generate_ca():
    # 这里可以生成CA(Client)
    return "CA(Client)"

def sign_message(ga, gb, n1, n2, ca):
    # 使用hmac实现数字签名
    key = str(gb).encode()
    data = f"{ga},{gb},{n1},{n2},{ca}".encode()
    return hmac.new(key, data, hashlib.sha256).hexdigest()

def verify_signature(ga, gb, n1, n2, sig_s):
    # 这里可以实现Sig_s验证逻辑
    return True  # 简单示例，始终返回True

if __name__ == "__main__":
    main()

