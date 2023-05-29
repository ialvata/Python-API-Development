"""
Utilities Module for main.py
"""

from passlib.context import CryptContext


####################     Password processing utilities         ###############################
def hash(password: str):
    pwd_hasher = CryptContext(schemes=["bcrypt"])
    return pwd_hasher.hash(password)
