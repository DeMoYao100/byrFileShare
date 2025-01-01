# Placeholder

def init(db_path: str = path) -> None:
    """Initialize the sqlite database"""
    path = db_path
    if os.path.exists(path):
        with sqlite3.connect(path) as db_conn:
            db_conn.execute('DELETE FROM AUTHCODE_INFO;')
        return
    with sqlite3.connect(path) as db_conn:
        db_conn.execute(
            '''
            CREATE TABLE USER_INFO (
                email TEXT PRIMARY KEY,
                pwdhash TEXT NOT NULL,
                salt TEXT NOT NULL
            );
            '''
        )
        db_conn.execute(
            '''
            CREATE UNIQUE INDEX USER_email ON USER_INFO (email);
            '''
        )
        db_conn.execute(
            '''
            CREATE TABLE GROUP_INFO (
                id TEXT NOT NULL,
                member TEXT NOT NULL,
                PRIMARY KEY (id, member),
                FOREIGN KEY (member) REFERENCES USER_INFO (email) ON DELETE CASCADE
            );
            '''
        )
        db_conn.execute(
            '''
            CREATE INDEX GROUP_id ON GROUP_INFO (member);
            '''
        )
        db_conn.execute(
            '''
            CREATE TABLE AUTHCODE_INFO (
                email TEXT PRIMARY KEY,
                authcode TEXT NOT NULL,
                timestamp INTEGER NOT NULL
            );
            '''
        )




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



