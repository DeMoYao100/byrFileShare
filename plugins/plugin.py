# Placeholder

def handle_del_dir(conn: socket.socket, key, email: str, msg: dict):
    print(f'\033[32m{addr[0].rjust(15)}:{addr[1]:5}\033[0m Request del-dir')
    if services.del_dir(msg['id'], msg['path']) == model.FileOpStatus.Ok:
        crypt_send_msg(conn, key, {'status': 200})
    else:
        crypt_send_msg(conn, key, {'status': 400})




def load_certificate_file(file_name):
    try:
        with open(file_name, 'r') as file:
            certificate = file.read()
        return certificate
    except FileNotFoundError:
        print(f"�ļ� {file_name} δ�ҵ�")
        return None
    except IOError:
        print("�ļ���ȡ����")
        return None



