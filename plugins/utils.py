# Placeholder

def put_file(prefix: str, full_name: str, content: bytes) -> FileOpStatus:
    """Put a file to the user's path or group's path

    Args:
        prefix (str): The email of the user or the id of the group
        full_name (str): The path of the file (including file name)
        content (bytes): The content of the file

    Returns:
        FileOpStatus: The status of the operation
    """
    if '@' in prefix:
        path_prefix = hashlib.md5(prefix.encode()).hexdigest()
    else:
        path_prefix = prefix
    full_path = os.path.join(path_prefix, full_name)
    if not file.put_file(full_path, content):
        return FileOpStatus.Collision
    return FileOpStatus.Ok




def del_dir(prefix: str, full_path: str) -> FileOpStatus:
    """Delete a directory and all files in it (or a single file) to the user's path or group's path

    Args:
        prefix (str): The email of the user or the id of the group
        full_path (str): The full path of the directory

    Returns:
        FileOpStatus: The status of the operation
    """
    if '@' in prefix:
        path_prefix = hashlib.md5(prefix.encode()).hexdigest()
    else:
        path_prefix = prefix
    full_path = os.path.join(path_prefix, full_path)
    if not file.del_dir(full_path):
        return FileOpStatus.PathErr
    return FileOpStatus.Ok



