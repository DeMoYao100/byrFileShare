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



