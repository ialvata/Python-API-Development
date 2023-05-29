"""
Utilities Module for main.py
"""

from passlib.context import CryptContext

####################     Password processing utilities         ###############################
pwd_hasher = CryptContext(schemes=["bcrypt"])


def hash(password: str):
    return pwd_hasher.hash(password)


def verify(password: str, hashed_password: str):
    return pwd_hasher.verify(password, hashed_password)
