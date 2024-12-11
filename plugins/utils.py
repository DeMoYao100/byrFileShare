# Placeholder

def check_path(prefix: str, full_path: str) -> bool:
    """Check if the directory exists

    Args:
        prefix (str): The email of the user or the id of the group
        full_path (str): The full path of the directory

    Returns:
        bool: True if exists, False otherwise
    """
    if '@' in prefix:
        path_prefix = hashlib.md5(prefix.encode()).hexdigest()
    else:
        path_prefix = prefix
    full_path = os.path.join(path_prefix, full_path)
    return file.check_path(full_path)



