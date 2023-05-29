"""
Module responsible for pydantic models/schemas
"""
# pylint: disable = too-few-public-methods

from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Class responsible for the `posts` table in the PostgreSQL DB
    """

    email: EmailStr


class UserInDB(UserBase):
    hashed_password: str


class UserCreate(UserBase):
    """
    Class responsible for the `posts` table in the PostgreSQL DB
    """

    password: str


class UserResponse(UserBase):
    """
    Class responsible for the `posts` table in the PostgreSQL DB
    """

    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        """
        Class responsible for compatibility between SQLAlchemy schemas and Pydantic models.
        """

        orm_mode = True


class UserLogin(UserBase):
    """
    Class responsible for the `posts` table in the PostgreSQL DB
    """

    password: str

    class Config:
        """
        Class responsible for compatibility between SQLAlchemy schemas and Pydantic models.
        """

        orm_mode = True
