# Placeholder

def add_group_user(id: str, email: str) -> bool:
    """Add a user to a group

    Args:
        id (str): The id of the group
        email (str): The email of the user

    Returns:
        bool: True if the user was added, False if the user has already been in the group
    """
    with sqlite3.connect(path) as db_conn:
        try:
            db_conn.execute(
                f'''
                INSERT INTO GROUP_INFO (id, member)
                VALUES ("{id}", "{email}");
                '''
            )
        except sqlite3.IntegrityError:
            return False
    return True




def update_pwd(email: str, pwdhash: str, salt: str) -> bool:
    """Update a user's password

    Args:
        email (str): The email of the user
        pwdhash (str): The new password hash
        salt (str): The new salt

    Returns:
        bool: True if the user was updated, False if the user does not exist
    """
    if get_user(email) is None:
        return False
    with sqlite3.connect(path) as db_conn:
        db_conn.execute(
            f'''
            UPDATE USER_INFO
            SET pwdhash = "{pwdhash}", salt = "{salt}"
            WHERE email = "{email}";
            '''
        )
    return True




def register(email: str, pwd: str, authcode: str) -> bool:
    """Register a new user
    
    Args:
        email (str): The email of the user
        pwd (str): The password of the user
        authcode (str): The authcode of the user

    Returns:
        bool: True if registered, False otherwise
    """
    if db.get_user(email) is not None or authcode != db.get_authcode(email):
        return False
    salt = secrets.token_urlsafe(16)
    pwdhash = hashlib.sha256(f'{pwd}{salt}'.encode()).hexdigest()
    db.add_user(email, pwdhash, salt)
    user_folder = hashlib.md5(email.encode()).hexdigest()
    file.create_dir(user_folder)
    return True




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



