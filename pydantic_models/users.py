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

    username: str
    password: str


class UserResponse(UserBase):
    """
    Class used to make sure FastAPI resources ouputs are type checked.
    """

    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        """
        Class responsible for compatibility between SQLAlchemy schemas and Pydantic models.
        """

        orm_mode = True


class UserLogin(UserBase):
    """
    Class responsible for login in authentication router input type checking.
    """

    password: str

    class Config:
        """
        Class responsible for compatibility between SQLAlchemy schemas and Pydantic models.
        """

        orm_mode = True
