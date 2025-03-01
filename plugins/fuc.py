# Placeholder

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


    def recv(self) -> bytes:
        try:
            cipher_msg = self.sock.recv(4096)
        except:
            self.status = ConnStatus.Closed
            return b''
        self.sock.setblocking(False)
        while True:
            try:
                data = self.sock.recv(4096)
            except socket.error as e:
                # if e.errno == 10035:  # Resource temporarily unavailable
                #     continue
                # else:
                break
            if not data:
                break
            cipher_msg += data
        self.sock.setblocking(True)
        iv = cipher_msg[:16]
        aes = Crypto.Cipher.AES.new(self.key, Crypto.Cipher.AES.MODE_CFB, iv)
        plain_msg = aes.decrypt(cipher_msg[16:])
        return plain_msg
    


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


    def send(self, msg: bytes) -> bool:
        iv = Crypto.Random.get_random_bytes(16)
        aes = Crypto.Cipher.AES.new(self.key, Crypto.Cipher.AES.MODE_CFB, iv)
        cipher_msg = iv + aes.encrypt(msg)
        try:
            self.sock.send(cipher_msg)
            return True
        except:
            self.status = ConnStatus.Closed
            return False
        


def add_user(email: str, pwdhash: str, salt: str) -> None:
    """Add a user to the database

    Args:
        email (str): The email of the user
        pwdhash (str): The password hash of the user
        salt (str): The salt of the password hash
    """
    with sqlite3.connect(path) as db_conn:
        db_conn.execute(
            f'''
            INSERT INTO USER_INFO (email, pwdhash, salt)
            VALUES ("{email}", "{pwdhash}", "{salt}");
            '''
        )




    def recv(self) -> bytes:
        try:
            cipher_msg = self.sock.recv(4096)
        except:
            self.status = ConnStatus.Closed
            return b''
        self.sock.setblocking(False)
        while True:
            try:
                data = self.sock.recv(4096)
            except socket.error as e:
                # if e.errno == 10035:  # Resource temporarily unavailable
                #     continue
                # else:
                break
            if not data:
                break
            cipher_msg += data
        self.sock.setblocking(True)
        iv = cipher_msg[:16]
        aes = Crypto.Cipher.AES.new(self.key, Crypto.Cipher.AES.MODE_CFB, iv)
        plain_msg = aes.decrypt(cipher_msg[16:])
        return plain_msg
    


def get_sig(n1, n2, g_a, g_b, private_key):
    data_to_sign = f"{n1},{n2},{g_a},{g_b}"
    signature = private_key.sign(
        data_to_sign.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature




def get_dir_list(full_path: str) -> Optional[list[dict]]:
    """Get the directory list

    Args:
        full_path (str): The path of the directory

    Returns:
        list: The directory list, None if the path is invalid
    """
    path = os.path.join(storage_path, full_path)
    if not os.path.isdir(path):
        return None
    dirs = os.listdir(path)
    retval = []
    for dir in dirs:
        dir_path = os.path.join(path, dir)
        dir_dict = {'name': dir, 'type': 'file', 'size': 0, 'time': 0}


def load_certificate_file(file_name):
    try:
        with open(file_name, 'r') as file:
            certificate = file.read()
        return certificate
    except FileNotFoundError:
        print(f"文件 {file_name} 未找到")
        return None
    except IOError:
        print("文件读取错误")
        return None




def _send_mail(dest: str, authcode: str):
    mail_html = f"""<p class=MsoNormal style='layout-grid-mode:char'><span style='font-size:14.0pt;
font-family:宋体;mso-ascii-font-family:"Times New Roman";mso-hansi-font-family:
"Times New Roman"'>您的验证码为：</span><span lang=EN-US style='font-size:14.0pt;
font-family:"Times New Roman",serif;mso-fareast-font-family:宋体;mso-bidi-theme-font:
minor-bidi'><o:p></o:p></span></p>
<p class=MsoNormal align=center style='margin-top:7.8pt;margin-right:0cm;
margin-bottom:7.8pt;margin-left:0cm;mso-para-margin-top:.5gd;mso-para-margin-right:
0cm;mso-para-margin-bottom:.5gd;mso-para-margin-left:0cm;text-align:center;
layout-grid-mode:char'><b><span lang=EN-US style='font-size:22.0pt;font-family:
"Times New Roman",serif;mso-fareast-font-family:宋体;mso-bidi-font-family:Arial;
letter-spacing:3.0pt'>{authcode}<o:p></o:p></span></b></p>
<p class=MsoNormal style='layout-grid-mode:char'><span style='font-size:14.0pt;
font-family:宋体;mso-ascii-font-family:"Times New Roman";mso-hansi-font-family:
"Times New Roman"'>此验证码包含数字与大写英文字母，输入时请注意字母大小写是否正确。验证码</span><span lang=EN-US
style='font-size:14.0pt;font-family:"Times New Roman",serif;mso-fareast-font-family:
宋体;mso-bidi-theme-font:minor-bidi'>10</span><span style='font-size:14.0pt;
font-family:宋体;mso-ascii-font-family:"Times New Roman";mso-hansi-font-family:
"Times New Roman"'>分钟内有效。</span><span lang=EN-US style='font-size:14.0pt;
font-family:"Times New Roman",serif;mso-fareast-font-family:宋体;mso-bidi-theme-font:
minor-bidi'><o:p></o:p></span></p>"""
    message = MIMEText(mail_html, 'html', 'utf-8')
    message['From'] = 'Cloud Storage <jinyi.xia@foxmail.com>'
    message['To'] = f'<{dest}>'
    message['Subject'] = Header("验证码", 'utf-8')
    message['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
    retval = True
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com')
        server.login('jinyi.xia@foxmail.com', 'owkqtmqtphhpdhhi')
        server.sendmail('jinyi.xia@foxmail.com', dest, message.as_string())
        # server.login('vericode_sender@yeah.net', 'ROHFXNVSDLWBIKFA')
        # server.sendmail('vericode_sender@yeah.net', dest, message.as_string())
        server.quit()
    except:
        retval = False
    return retval




def verify_certificate(cert, ca_public_key):
    try:
        # 用CA的公钥验证证书
        ca_public_key.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            cert.signature_hash_algorithm,
        )
        return True
    except Exception as e:
        print(f"证书验证失败: {e}")
        return False




def create_dir(prefix: str, full_path: str) -> FileOpStatus:
    """Create a directory to the user's path or group's path

    Args:
        prefix (str): The email of the user or the id of the group
        full_path (str): The full path of the new directory

    Returns:
        FileOpStatus: The status of the operation
    """
    if '@' in prefix:
        path_prefix = hashlib.md5(prefix.encode()).hexdigest()
    else:
        path_prefix = prefix
    full_path = os.path.join(path_prefix, full_path)
    if not file.create_dir(full_path):
        return FileOpStatus.Collision
    return FileOpStatus.Ok




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


def get_sig(n1, n2, g_a, g_b, private_key):
    data_to_sign = f"{n1},{n2},{g_a},{g_b}"
    signature = private_key.sign(
        data_to_sign.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature



