# Placeholder

def receive_file(filename, sock):
    with open(filename, "wb") as f:
        data = sock.recv(4096)
        f.write(data)
        sock.setblocking(False)  # ���׽�������Ϊ������ģʽ
        while True:
            try:
                data = sock.recv(4096)
            except socket.error as e:
                # if e.errno == 10035:  # ����� "Resource temporarily unavailable" ���������ѭ��
                #     continue
                # else:
                break
            if not data:
                break
            f.write(data)
    sock.setblocking(True)



