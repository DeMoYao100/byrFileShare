import db
from model import User


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
