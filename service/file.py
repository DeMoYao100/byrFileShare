import os
from typing import Optional
import shutil


storage_path = './storage/'


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
        if os.path.isdir(dir_path):
            dir_dict['type'] = 'dir'
        dir_dict['size'] = None if dir_dict['type'] == 'dir' else os.path.getsize(dir_path)
        dir_dict['time'] = int(os.path.getmtime(dir_path))
        retval.append(dir_dict)
    return retval


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
    

def check_path(full_path: str) -> bool:
    """Check if the path exists

    Args:
        full_path (str): The path to check

    Returns:
        bool: True if the path is valid, False otherwise
    """
    path = os.path.join(storage_path, full_path)
    return os.path.exists(path)


def put_file(full_name: str, content: bytes) -> bool:
    """Put a file to the path

    Args:
        full_name (str): The path of the file (including file name)
        content (bytes): The content of the file

    Returns:
        bool: True if the file was put, False otherwise
    """
    path = os.path.join(storage_path, full_name)
    if os.path.exists(path):
        return False
    with open(path, 'wb') as f:
        f.write(content)
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


def del_dir(full_path: str) -> bool:
    """Delete a directory to the path

    Args:
        full_path (str): The full path of the directory

    Returns:
        bool: True if the directory was deleted, False otherwise
    """
    path = os.path.join(storage_path, full_path)
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)
    else:
        return False
    return True


if __name__ == '__main__':
    storage_path = '.'
    # print(create_dir('test'))
    # print(put_file('test/111',b'0x12'))
    # print(check_path('test/111'))
    print(get_dir_list('.'))
    # print(get_file('test/111'))
    # print(del_dir('test'))