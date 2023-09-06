import services
import socket
import threading
import json
import os
import hashlib
import model
import time
import base64
from SignatureSystem import get_sig
from CA_verify import load_certificate_file
import Crypto.PublicKey.RSA
import Crypto.Cipher.PKCS1_v1_5
import Crypto.Random
import Crypto.Cipher.AES
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


host = '0.0.0.0'
port = 2057


def receive_file(filename, sock):
    with open(filename, "wb") as f:
        data = sock.recv(4096)
        f.write(data)
        sock.setblocking(False)  # 将套接字设置为非阻塞模式
        while True:
            try:
                data = sock.recv(4096)
            except socket.error as e:
                # if e.errno == 10035:  # 如果是 "Resource temporarily unavailable" 错误，则继续循环
                #     continue
                # else:
                break
            if not data:
                break
            f.write(data)
    sock.setblocking(True)


def recv_long(conn: socket.socket) -> bytes:
    msg = conn.recv(4096)
    conn.setblocking(False)
    while True:
        try:
            data = conn.recv(4096)
        except socket.error as e:
            # if e.errno == 10035:  # Resource temporarily unavailable
            #     continue
            # else:
            break
        if not data:
            break
        msg += data
    conn.setblocking(True)
    return msg


def crypt_send_bytes(conn: socket.socket, key: bytes, msg: bytes):
    iv = Crypto.Random.get_random_bytes(16)
    aes = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, iv)
    cipher_msg = iv + aes.encrypt(msg)
    conn.send(cipher_msg)


def crypt_recv_bytes(conn: socket.socket, key) -> bytes:
    cipher_msg = conn.recv(4096)
    iv = cipher_msg[:16]
    aes = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, iv)
    plain_msg = aes.decrypt(cipher_msg[16:])
    return plain_msg


def crypt_send_msg(conn: socket.socket, key, msg: dict):
    plain_msg = json.dumps(msg).encode()
    crypt_send_bytes(conn, key, plain_msg)


def crypt_recv_msg(conn: socket.socket, key) -> dict:
    plain_msg = crypt_recv_bytes(conn, key)
    return json.loads(plain_msg.decode())


def handle_gen_authcode(conn: socket.socket, key, email: str, msg: dict):
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request gen-authcode')
    if services.gen_authcode(email):
        crypt_send_msg(conn, key, {'status': 200})
    else:
        crypt_send_msg(conn, key, {'status': 400})


def handle_pwd_login(conn: socket.socket, key, email: str, msg: dict) -> bool:
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request pwd-login')
    if services.pwd_login_verify(email, msg['pwd']):
        crypt_send_msg(conn, key, {'status': 200})
        return True
    else:
        crypt_send_msg(conn, key, {'status': 400})
        return False


def handle_authcode_login(conn: socket.socket, key, email: str, msg: dict) -> bool:
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request authcode-login')
    if services.authcode_login_verify(email, msg['authcode']):
        crypt_send_msg(conn, key, {'status': 200})
        return True
    else:
        crypt_send_msg(conn, key, {'status': 400})
        return False


def handle_update_pwd(conn: socket.socket, key, email: str, msg: dict) -> bool:
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request update-pwd')
    if services.update_pwd(email, msg['pwd'], msg['authcode']):
        crypt_send_msg(conn, key, {'status': 200})
        return True
    else:
        crypt_send_msg(conn, key, {'status': 400})
        return False


def handle_register(conn: socket.socket, key, email: str, msg: dict) -> bool:
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request register')
    if services.register(email, msg['pwd'], msg['authcode']):
        crypt_send_msg(conn, key, {'status': 200})
        return True
    else:
        crypt_send_msg(conn, key, {'status': 400})
        return False


def handle_get_dir_list(conn: socket.socket, key, email: str, msg: dict):
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request get-dir-list')
    result = services.get_dir_list(msg['id'], msg['path'])
    if result is None:
        crypt_send_msg(conn, key, {'status': 400, 'list': []})
    else:
        crypt_send_msg(conn, key, {'status': 200, 'list': result})


def handle_put_file(conn: socket.socket, key, email: str, msg: dict):
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request put-file')
    if services.check_path(msg['id'], msg['path']):
        crypt_send_bytes(conn, key, b'400')
        return
    else:
        crypt_send_bytes(conn, key, b'200')
    if crypt_recv_bytes(conn, key) == b'200':
        crypt_send_bytes(conn, key, b'200')
    else:
        crypt_send_bytes(conn, key, b'400')
        return
    fifo_path = f'./tmp/{int(time.time())}.pipe'
    receive_file(fifo_path, conn)
    with open(fifo_path, 'rb') as f:
        cipher_msg = f.read()
    iv = cipher_msg[:16]
    aes = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, iv)
    plain_msg = aes.decrypt(cipher_msg[16:])
    services.put_file(msg['id'], msg['path'], plain_msg)
    crypt_send_msg(conn, key, {'status': 200})


def handle_create_dir(conn: socket.socket, key, email: str, msg: dict):
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request create-dir')
    if services.create_dir(msg['id'], msg['path']) == model.FileOpStatus.Ok:
        crypt_send_msg(conn, key, {'status': 200})
    else:
        crypt_send_msg(conn, key, {'status': 400})


def handle_del_dir(conn: socket.socket, key, email: str, msg: dict):
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request del-dir')
    if services.del_dir(msg['id'], msg['path']) == model.FileOpStatus.Ok:
        crypt_send_msg(conn, key, {'status': 200})
    else:
        crypt_send_msg(conn, key, {'status': 400})


def handle_get_file(conn: socket.socket, key, email: str, msg: dict):
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request get-file')
    result = services.get_file(msg['id'], msg['path'])
    if result is None:
        crypt_send_bytes(conn, key, b'\x00')
    else:
        crypt_send_bytes(conn, key, result)


def handle_join_group(conn: socket.socket, key, email: str, msg: dict):
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request join-group')
    if services.join_group(email, msg['id']):
        crypt_send_msg(conn, key, {'status': 200})
    else:
        crypt_send_msg(conn, key, {'status': 400})


def server_thread(conn: socket.socket, addr: tuple[str, int]):
    is_logined = False
    key = None
    email = ''
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Connected')
    
    # build channel
    p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
    g = 2
    n1 = int(conn.recv(4096).decode()) # recv
    n2 = int(os.urandom(32).hex(), 16)
    a = int(os.urandom(32).hex(), 16)
    g_a = pow(g, a, p)
    # 从文件中读取CA
    CA_name = "user_cert.pem"
    CA = load_certificate_file(CA_name)
    conn.send(json.dumps({"n2": n2, "g_a": g_a, "CA": base64.b64encode(CA.encode()).decode('utf-8')}).encode()) # send
    g_b = int(conn.recv(1024).decode()) # recv
    key = pow(g_b, a, p)
    key_bytes = key.to_bytes(256, byteorder='big')
    sha256 = hashlib.sha256()
    sha256.update(key_bytes)
    key = sha256.digest()
    # 计算签名并发送
    private_key = None
    with open("user_private_key.pem", 'rb') as file:
        pem_private = file.read()
    private_key = serialization.load_pem_private_key(pem_private, password=None, backend=default_backend())
    sig_s = get_sig(n1, n2, g_a, g_b, private_key)
    conn.send(sig_s) # send

    while True:
        try:
            msg_bytes = crypt_recv_bytes(conn, key)
            msg = json.loads(msg_bytes.decode())
        except:
            print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Connection closed')
            conn.close()
            break
        if msg['op'] == 'gen-authcode':
            email = msg['email']
            handle_gen_authcode(conn, key, email, msg)
        elif msg['op'] == 'pwd-login':
            email = msg['email']
            is_logined = handle_pwd_login(conn, key, email, msg)
        elif msg['op'] == 'authcode-login':
            email = msg['email']
            is_logined = handle_authcode_login(conn, key, email, msg)
        elif msg['op'] == 'update-pwd':
            email = msg['email']
            is_logined = handle_update_pwd(conn, key, email, msg)
        elif msg['op'] == 'register':
            email = msg['email']
            is_logined = handle_register(conn, key, email, msg)
        elif msg['op'] == 'get-dir-list':
            if not is_logined:
                crypt_send_msg(conn, key, {'status': 400, 'list': []})
                continue
            handle_get_dir_list(conn, key, email, msg)
        elif msg['op'] == 'put-file':
            if not is_logined:
                crypt_send_bytes(conn, key, b'400')
                continue
            handle_put_file(conn, key, email, msg)
        elif msg['op'] == 'create-dir':
            if not is_logined:
                crypt_send_msg(conn, key, {'status': 400, 'list': []})
                continue
            handle_create_dir(conn, key, email, msg)
        elif msg['op'] == 'del-dir':
            if not is_logined:
                crypt_send_msg(conn, key, {'status': 400, 'list': []})
                continue
            handle_del_dir(conn, key, email, msg)
        elif msg['op'] == 'get-file':
            if not is_logined:
                crypt_send_bytes(conn, key, b'\x00')
                continue
            handle_get_file(conn, key, email, msg)
        elif msg['op'] == 'join-group':
            if not is_logined:
                crypt_send_msg(conn, key, {'status': 400, 'list': []})
                continue
            handle_join_group(conn, key, email, msg)
        else:
            crypt_send_msg(conn, key, {'status': 400})
            print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Invalid operation')


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(16)
    print(f'Server running at {host}:{port}')
    while True:
        conn, addr = sock.accept()
        thread = threading.Thread(target=server_thread, args=(conn, addr))
        thread.daemon = True
        thread.start()