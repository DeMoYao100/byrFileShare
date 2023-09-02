import sqlite3
from typing import Optional
from model import User, Group


path = 'cloud_storage.db'


def init() -> None:
    """Initialize the sqlite database and create blank tables
    
    Run this function if the database does not exist
    """
    pass


def get_user(email: str) -> Optional[User]:
    """Get a user's info by email

    Args:
        email (str): The email of the user

    Returns:
        Optional[User]: The user object if found, None otherwise
    """
    return User()


def add_user(user: User) -> bool:
    """Add a user to the database

    Args:
        user (User): The user to add

    Returns:
        bool: True if the user was added, False if the user has already existed
    """
    return False


def update_pwd(user: User) -> bool:
    """Update a user's password

    Args:
        user (User): The user to update

    Returns:
        bool: True if the user was updated, False if the user does not exist
    """
    return False


def get_group_by_user(email: str) -> list[str]:
    """Get a list of group ids that a user is a member of

    Args:
        email (str): The email of the user

    Returns:
        list[str]: A list of group ids
    """
    return []


def get_group_by_id(id: str) -> Group:
    """Get a group by its id

    Args:
        id (str): The id of the group

    Returns:
        Group: The group object
    """
    return Group()


def create_group(group: Group) -> bool:
    """Create a group

    Args:
        group (Group): The group to create

    Returns:
        bool: True if the group was created, False if the group has already existed
    """
    return False


def add_group_user(id: str, email: str) -> bool:
    """Add a user to a group

    Args:
        id (str): The id of the group
        email (str): The email of the user

    Returns:
        bool: True if the user was added, False if the user has already been in the group or the group does not exist
    """
    return False


def update_authcode(email: str, authcode: str) -> Optional[str]:
    """Update authcode by email

    Args:
        email (str): The email
        authcode (str): The authcode

    Returns:
        Optional[str]: The authcode if available, None otherwise
    """
    return None


def get_authcode(email: str) -> Optional[str]:
    """Get authcode by email

    Args:
        email (str): The email

    Returns:
        Optional[str]: The authcode if available, None otherwise
    """
    return None
