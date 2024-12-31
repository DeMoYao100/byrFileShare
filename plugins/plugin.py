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




def get_file(prefix: str, full_name: str) -> Optional[bytes]:
    """Get the file list of the user's path or group's path

    Args:
        prefix (str): The email of the user or the id of the group
        full_name (str): The path of the file (including file name)

    Returns:
        bytes: The file, None if the path is invalid or the user/group does not exist
    """
    if '@' in prefix:
        path_prefix = hashlib.md5(prefix.encode()).hexdigest()
    else:
        path_prefix = prefix
    return file.get_file(os.path.join(path_prefix, full_name))




    def __init__(self, email: Optional[str] = None, pwdhash: Optional[str] = None, salt: Optional[str] = None):
        """User object

        Args:
            email (Optional[str], optional): User's email. Defaults to None.
            pwdhash (Optional[str], optional): Hashcode of the user's password. Defaults to None.
            salt (Optional[str], optional): Salt of the hashcode. Defaults to None.
        """
        self.email = email
        self.pwdhash = pwdhash
        self.salt = salt


class Group:


    def __init__(self, email: Optional[str] = None, pwdhash: Optional[str] = None, salt: Optional[str] = None):
        """User object

        Args:
            email (Optional[str], optional): User's email. Defaults to None.
            pwdhash (Optional[str], optional): Hashcode of the user's password. Defaults to None.
            salt (Optional[str], optional): Salt of the hashcode. Defaults to None.
        """
        self.email = email
        self.pwdhash = pwdhash
        self.salt = salt


class Group:


    def close(self) -> None:
        self.sock.close()
        self.status = ConnStatus.Closed


