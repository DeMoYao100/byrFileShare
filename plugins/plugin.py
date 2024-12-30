# Placeholder

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



