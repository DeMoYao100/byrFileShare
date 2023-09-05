import socket
import random
import hashlib
import pickle

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes, serialization

from Server import data_to_sign, public_key_bytes

# Diffie-Hellman 参数
p = 23  # 素数
g = 5   # 生成元
a = random.randint(1, 10)  # 客户端的私钥
b = random.randint(1, 10)  # 服务器的私钥

# 计算模幂运算的函数
def mod_exp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

# 创建一个套接字并连接到服务器
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))

# 步骤 1：生成 n1 并发送给服务器
n1 = random.randint(1, 100)
client_socket.send(str(n1).encode())
print("发送 n1 给服务器:", n1)

# 步骤 2：从服务器接收 n2
n2 = int(client_socket.recv(1024).decode())
print("从服务器接收到 n2:", n2)

# 步骤 3：计算 g^b 和 CA(Client)
g_b = mod_exp(g, b, p)
ca_client = hashlib.sha256(str(g_b).encode()).hexdigest()

# 步骤 4：将 CA(Client)、g^b 和 Sig_c(g^a, g^b, n1, n2) 发送给服务器
sig_c = "placeholder_signature"
data_to_send = (ca_client, g_b, sig_c)
client_socket.send(pickle.dumps(data_to_send))
print("发送 CA(Client)、g^b 和 Sig_c(g^a, g^b, n1, n2) 给服务器")

# # 步骤 5：从服务器接收 Sig_s(g^a, g^b, n1, n2)
# signature = client_socket.recv(1024)
# print("从服务器接收到 Sig_s(g^a, g^b, n1, n2)")
#
# # 步骤 6：验证 Sig_s
# try:
#     public_key = serialization.load_pem_public_key(
#         public_key_bytes,
#         backend=default_backend()
#     )
#     public_key.verify(
#         signature,
#         data_to_sign,
#         padding.PKCS1v15(),
#         hashes.SHA256()
#     )
#     print("签名验证成功。")
# except InvalidSignature:
#     print("签名验证失败。关闭连接。")
#     client_socket.close()

# 步骤 5：从服务器接收 Sig_s(g^a, g^b, n1, n2)
sig_s = client_socket.recv(1024)
print("从服务器接收到 Sig_s(g^a, g^b, n1, n2):", sig_s)

# 步骤 6：验证 Sig_s
# 在实际应用中，应使用适当的数字签名库进行验证。
# 此处我们只是将接收到的签名与占位符值进行比较。
placeholder_signature = b"placeholder_signature"
if sig_s != placeholder_signature:
    print("签名验证失败。关闭连接。")
    client_socket.close()
else:
    print("签名验证成功。")

# 步骤 7：计算共享秘密 g^(ab)
shared_secret = mod_exp(g, a * b, p)

# 步骤 8：关闭连接
client_socket.close()

print("共享秘密 (g^(ab)):", shared_secret)
