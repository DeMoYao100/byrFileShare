import db
import file
from typing import Optional
from model import FileOpStatus


def gen_authcode(email: str) -> bool:
    """Generate authcode by email
    
    Args:
        email (str): The email of the user

    Returns:
        bool: True if the authcode was sent, False otherwise
    """
    return False


def pwd_login_verify(email: str, pwd: str) -> bool:
    """Verify login by email and password
    
    Args:
        email (str): The email of the user
        pwd (str): The password of the user

    Returns:
        bool: True if verified, False otherwise
    """
    return False


def authcode_login_verify(email: str, authcode: str) -> bool:
    """Verify login by email and authcode
    
    Args:
        email (str): The email of the user
        authcode (str): The authcode of the user

    Returns:
        bool: True if verified, False otherwise
    """
    return False


def register(email: str, pwd: str, authcode: str) -> bool:
    """Register a new user
    
    Args:
        email (str): The email of the user
        pwd (str): The password of the user
        authcode (str): The authcode of the user

    Returns:
        bool: True if registered, False otherwise
    """
    return False


def get_dir_list(suffix: str, path: str) -> Optional[list]:
    """Get the directory list of the user's path or group's path

    Args:
        suffix (str): The email of the user or the id of the group
        path (str): The path of the directory

    Returns:
        list: The directory list, None if the path is invalid or the user/group does not exist
    """
    return None


def get_file(suffix: str, full_name: str) -> Optional[bytes]:
    """Get the file list of the user's path or group's path

    Args:
        suffix (str): The email of the user or the id of the group
        full_name (str): The path of the file (including file name)

    Returns:
        list: The file, None if the path is invalid or the user/group does not exist
    """
    return None


def put_file(suffix: str, full_name: str, content: bytes) -> FileOpStatus:
    """Put a file to the user's path or group's path

    Args:
        suffix (str): The email of the user or the id of the group
        full_name (str): The path of the file (including file name)
        content (bytes): The content of the file

    Returns:
        FileOpStatus: The status of the operation
    """
    return FileOpStatus.Ok


def create_dir(suffix: str, full_path: str) -> FileOpStatus:
    """Create a directory to the user's path or group's path

    Args:
        suffix (str): The email of the user or the id of the group
        full_path (str): The full path of the new directory

    Returns:
        FileOpStatus: The status of the operation
    """
    return FileOpStatus.Ok


def del_dir(suffix: str, full_path: str) -> FileOpStatus:
    """Delete a directory and all files in it to the user's path or group's path

    Args:
        suffix (str): The email of the user or the id of the group
        full_path (str): The full path of the directory

    Returns:
        FileOpStatus: The status of the operation
    """
    return FileOpStatus.Ok


def del_file(suffix: str, full_name: str) -> FileOpStatus:
    """Delete a file to the user's path or group's path

    Args:
        suffix (str): The email of the user or the id of the group
        full_name (str): The path of the file (including file name)

    Returns:
        FileOpStatus: The status of the operation
    """
    return FileOpStatus.Ok


def join_group(email: str, id: str) -> bool:
    """Join a group
    
    Args:
        email (str): The email of the user
        id (str): The id of the group

    Returns:
        bool: True if joined, False otherwise
    """
    return False