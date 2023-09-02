import os
from typing import Optional


storage_path = './storage'


def get_dir_list(full_path: str) -> Optional[list]:
    """Get the directory list

    Args:
        full_path (str): The path of the directory

    Returns:
        list: The directory list, None if the path is invalid
    """
    if not os.path.isdir(full_path):
        return None
    return os.listdir(full_path)


def get_file(full_name: str) -> Optional[bytes]:
    """Get the file

    Args:
        full_name (str): The path of the file (including file name)

    Returns:
        list: The file, None if the path is invalid
    """
    if not os.path.isfile(full_name):
        return None
    with open(full_name, 'rb') as f:
        return f.read()
    

def check_path(full_path: str) -> bool:
    """Check if the path exists

    Args:
        full_path (str): The path to check

    Returns:
        bool: True if the path is valid, False otherwise
    """
    if not os.path.exists(full_path):
        return False
    return True


def put_file(full_name: str, content: bytes) -> bool:
    """Put a file to the path

    Args:
        full_name (str): The path of the file (including file name)
        content (bytes): The content of the file

    Returns:
        bool: True if the file was put, False otherwise
    """
    if os.path.exists(full_name):
        return False
    with open(full_name, 'wb') as f:
        f.write(content)
    return True


def create_dir(full_path: str) -> bool:
    """Create a directory to the path

    Args:
        full_path (str): The full path of the new directory

    Returns:
        bool: True if the directory was created, False otherwise
    """
    if os.path.exists(full_path):
        return False
    os.mkdir(full_path)
    return True


def del_dir(full_path: str) -> bool:
    """Delete a directory to the path

    Args:
        full_path (str): The full path of the directory

    Returns:
        bool: True if the directory was deleted, False otherwise
    """
    return False


if __name__ == '__main__':
    pass
# service/file.py