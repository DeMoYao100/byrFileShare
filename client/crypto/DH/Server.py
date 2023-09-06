import socket
import random
import hashlib
import pickle
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

# Diffie-Hellman 参数
p = 23  # 素数
g = 5   # 生成元
a = random.randint(1, 10)  # 服务器的私钥

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

# 创建一个套接字并绑定到地址
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen(1)

print("服务器正在监听...")

conn, addr = server_socket.accept()

# 步骤 1：从客户端接收 n1
n1 = int(conn.recv(1024).decode())
print("从客户端接收到 n1:", n1)

# 步骤 2：生成 n2 并发送给客户端
n2 = random.randint(1, 100)
conn.send(str(n2).encode())
print("发送 n2 给客户端:", n2)

# 步骤 3：计算 g^a 和 CA(Server)
g_a = mod_exp(g, a, p)
ca_server = hashlib.sha256(str(g_a).encode()).hexdigest()

# 步骤 4：将 g^a 和 CA(Server) 发送给客户端
data_to_send = (g_a, ca_server)
conn.send(pickle.dumps(data_to_send))
print("发送 g^a 和 CA(Server) 给客户端")

# 步骤 5：从客户端接收 CA(Client)、g^b 和 Sig_c(g^a, g^b, n1, n2)
received_data = pickle.loads(conn.recv(1024))
ca_client, g_b, sig_c = received_data

# 验证 CA(Client)
if hashlib.sha256(str(g_b).encode()).hexdigest() != ca_client:
    print("CA(Client) 验证失败。关闭连接。")
    conn.close()
else:
    print("CA(Client) 验证成功。")

# 验证 Sig_c
# 在实际应用中，应使用适当的数字签名库进行验证。
# 此处我们只是将接收到的签名与占位符值进行比较。
placeholder_signature = "placeholder_signature"
if sig_c != placeholder_signature:
    print("签名验证失败。关闭连接。")
    conn.close()
else:
    print("签名验证成功。")

# 步骤 6：计算共享秘密 g^(ab)
shared_secret = mod_exp(g_b, a, p)

# 步骤 7：计算共享秘密 g^(ab)
shared_secret = mod_exp(g_b, a, p)

# 步骤 8：生成服务器端的私钥和公钥对
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# 将私钥序列化为字节字符串以供保存或传输
private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# 将公钥序列化为字节字符串以供传输给客户端
public_key = private_key.public_key()
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# 步骤 9：生成 Sig_s(g^a, g^b, n1, n2)
data_to_sign = f"{g_a}{g_b}{n1}{n2}".encode()
signature = private_key.sign(
    data_to_sign,
    padding.PKCS1v15(),
    hashes.SHA256()
)

# 将签名发送给客户端
conn.send(signature)

print("共享秘密 (g^(ab)):", shared_secret)
