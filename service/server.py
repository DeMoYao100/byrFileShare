import services
import socket
import threading
import json
import os
import hashlib
import model


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
                if e.errno == 10035:  # 如果是 "Resource temporarily unavailable" 错误，则继续循环
                    continue
                else:
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
            if e.errno == 10035:  # Resource temporarily unavailable
                continue
            else:
                break
        if not data:
            break
        msg += data
    conn.setblocking(True)
    return msg


def crypt_send_bytes(conn: socket.socket, key, msg: bytes):
    cipher_msg = msg
    conn.send(cipher_msg)


def crypt_recv_bytes(conn: socket.socket, key) -> bytes:
    cipher_msg = conn.recv(4096)
    plain_msg = cipher_msg
    return plain_msg


def crypt_send_msg(conn: socket.socket, key, msg: dict):
    plain_msg = json.dumps(msg).encode()
    cipher_msg = plain_msg
    conn.send(cipher_msg)


def crypt_recv_msg(conn: socket.socket, key) -> dict:
    cipher_msg = conn.recv(4096)
    plain_msg = cipher_msg
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
    if services.pwd_login_verify(email, msg['pwd']):
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
    if crypt_recv_bytes(conn, key) == b'200':
        crypt_send_bytes(conn, key, b'200')
    else:
        crypt_send_bytes(conn, key, b'400')
        return
    fifo_path = f'~/Secloud/tmp/{hashlib.md5(email.encode()).hexdigest()}.pipe'
    os.mkfifo(fifo_path)
    receive_file(fifo_path, conn)
    with open(fifo_path, 'rb') as f:
        crypt_msg = f.read()
    os.remove(fifo_path)
    plain_msg = crypt_msg
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
    while True:
        try:
            msg_bytes = conn.recv(4096)
            msg = json.loads(msg_bytes.decode())
        except:
            print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Connection Closed')
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
            handle_get_dir_list(conn, key, email, msg)
        elif msg['op'] == 'put-file':
            if not is_logined:
                crypt_send_bytes(conn, key, b'400')
            handle_put_file(conn, key, email, msg)
        elif msg['op'] == 'create-dir':
            if not is_logined:
                crypt_send_msg(conn, key, {'status': 400, 'list': []})
            handle_create_dir(conn, key, email, msg)
        elif msg['op'] == 'del-dir':
            if not is_logined:
                crypt_send_msg(conn, key, {'status': 400, 'list': []})
            handle_del_dir(conn, key, email, msg)
        elif msg['op'] == 'get-file':
            if not is_logined:
                crypt_send_bytes(conn, key, b'\x00')
            handle_get_file(conn, key, email, msg)
        elif msg['op'] == 'join-group':
            if not is_logined:
                crypt_send_msg(conn, key, {'status': 400, 'list': []})
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