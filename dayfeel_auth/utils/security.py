"""
Password hashing using Argon2id.
"""

# --- IMPORTS ---
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


# --- GLOBALS ---
PASSWORD_HASHER = PasswordHasher(
    time_cost=3,
    memory_cost=64 * 1024,
    parallelism=4,
    hash_len=32,
    salt_len=16
)


# --- CODE ---
def hash_password(password: str) -> str:
    """
    Generate hash from a password.

    :param password: The user's password.

    :returns: Password hash.
    """
    return PASSWORD_HASHER.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify whether a password matches the stored hash.

    :param password: The user's password.
    :param password_hash: The password hash previously stored in the database.

    :returns: True if the password matches the hash, False otherwise.
    """
    try:
        return PASSWORD_HASHER.verify(password_hash, password)
    except VerifyMismatchError:
        return False
