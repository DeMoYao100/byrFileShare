
def create_dir(full_path: str) -> bool:
    """Create a directory to the path

    Args:
        full_path (str): The full path of the new directory

    Returns:
        bool: True if the directory was created, False otherwise
    """
    path = os.path.join(storage_path, full_path)
    if os.path.exists(path):
        return False
    os.mkdir(path)
    return True




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




    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(('127.0.0.1', 2057))
            self.status = ConnStatus.Ok
        except:
            self.status = ConnStatus.Closed
        self.key = None

        p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
        g = 2
        n1 = int(os.urandom(32).hex(), 16)
        self.sock.send(str(n1).encode())
        
        # 接收，n2, g^a, CA(S)的json文件
        msg = self.sock.recv(4096)
        msg = json.loads(msg.decode())
        
        # 调用验证CA的算法
        n2 = msg['n2']
        g_a = msg['g_a']
        CA = base64.b64decode(msg['CA'])
        CA = x509.load_pem_x509_certificate(CA, default_backend())
        ca_public_pem_path = "ca_public_key.pem"
        with open(ca_public_pem_path, 'rb') as file:
            ca_public_pem = file.read()
        ca_public_pem = ca_public_pem
        ca_public_key = serialization.load_pem_public_key(ca_public_pem, backend=default_backend())
        pem_public = None
        if verify_certificate(CA, ca_public_key):
            pem_public = extract_public_key_from_certificate(CA)
        sig_public_key = serialization.load_pem_public_key(pem_public, backend=default_backend())
        b = int(os.urandom(32).hex(), 16)
        g_b = pow(g, b, p)
        self.sock.send(str(g_b).encode())

        # 接收并验证签名算法
        sig_s = self.sock.recv(4096)
        verify_sig(sig_s, n1, n2, g_a, g_b, sig_public_key)
 
        self.key = pow(g_a, b, p)
        key_bytes = self.key.to_bytes(256, byteorder='big')
        sha256 = hashlib.sha256()
        sha256.update(key_bytes)
        self.key = sha256.digest()



def get_file(full_name: str) -> Optional[bytes]:
    """Get the file

    Args:
        full_name (str): The path of the file (including file name)

    Returns:
        list: The file, None if the path is invalid
    """
    path = os.path.join(storage_path, full_name)
    if not os.path.isfile(path):
        return None
    with open(path, 'rb') as f:
        return f.read()
    



def authcode_login_verify(email: str, authcode: str) -> bool:
    """Verify login by email and authcode
    
    Args:
        email (str): The email of the user
        authcode (str): The authcode of the user

    Returns:
        bool: True if verified, False otherwise
    """
    expected = db.get_authcode(email)
    return expected == authcode




    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(('127.0.0.1', 2057))
            self.status = ConnStatus.Ok
        except:
            self.status = ConnStatus.Closed
        self.key = None

        p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
        g = 2
        n1 = int(os.urandom(32).hex(), 16)
        self.sock.send(str(n1).encode())
        
        # 接收，n2, g^a, CA(S)的json文件
        msg = self.sock.recv(4096)
        msg = json.loads(msg.decode())
        
        # 调用验证CA的算法
        n2 = msg['n2']
        g_a = msg['g_a']
        CA = base64.b64decode(msg['CA'])
        CA = x509.load_pem_x509_certificate(CA, default_backend())
        ca_public_pem_path = "ca_public_key.pem"
        with open(ca_public_pem_path, 'rb') as file:
            ca_public_pem = file.read()
        ca_public_pem = ca_public_pem
        ca_public_key = serialization.load_pem_public_key(ca_public_pem, backend=default_backend())
        pem_public = None
        if verify_certificate(CA, ca_public_key):
            pem_public = extract_public_key_from_certificate(CA)
        sig_public_key = serialization.load_pem_public_key(pem_public, backend=default_backend())
        b = int(os.urandom(32).hex(), 16)
        g_b = pow(g, b, p)
        self.sock.send(str(g_b).encode())

        # 接收并验证签名算法
        sig_s = self.sock.recv(4096)
        verify_sig(sig_s, n1, n2, g_a, g_b, sig_public_key)
 
        self.key = pow(g_a, b, p)
        key_bytes = self.key.to_bytes(256, byteorder='big')
        sha256 = hashlib.sha256()
        sha256.update(key_bytes)
        self.key = sha256.digest()



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




def get_groups(email: str) -> list[str]:
    """Get a list of groups ids that a user is a member of

    Args:
        email (str): The email of the user

    Returns:
        list[str]: A list of group ids
    """
    with sqlite3.connect(path) as db_conn:
        cursor = db_conn.execute(
            f'''
            SELECT id
            FROM GROUP_INFO
            WHERE member = "{email}"
            '''
        )
        all = cursor.fetchall()
    return [g[0] for g in all]



