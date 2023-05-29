"""
Module responsible for pydantic models/schemas
"""
# pylint: disable = too-few-public-methods

from datetime import datetime

from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    """
    Pydantic class that represents a Post
    """

    title: str
    content: str
    published: bool = True
    rating: float


class PostCreate(PostBase):
    """
    Pydantic class that represents a Post
    """

    title: str
    content: str
    published: bool = True
    rating: float = 0


class PostUpdate(PostBase):
    """
    Pydantic class that represents a Post
    """


class PostResponse(PostBase):
    """
    Pydantic class that represents a Post
    """

    # remaining attributes like content and title will be inherited from PostBase
    id: int
    created_at: datetime

    class Config:
        """
        Behaviour of pydantic can be controlled via the Config class on a model
        or a pydantic dataclass.
        Pydantic's `orm_mode` will tell the Pydantic model to read the data
        even if it is not a dict, but an ORM model
        (or any other arbitrary object with attributes).
        With this, the Pydantic model is compatible with ORMs, and you can just declare
        it in the response_model argument in your path operations.
        You will be able to return a database model and it will read the data from it.
        https://fastapi.tiangolo.com/tutorial/response-model/?h=
        """

        orm_mode = True


class UserBase(BaseModel):
    """
    Class responsible for the `posts` table in the PostgreSQL DB
    """

    email: EmailStr
    password: str


class UserCreate(UserBase):
    """
    Class responsible for the `posts` table in the PostgreSQL DB
    """


class UserResponse(BaseModel):
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


class UserLogin(BaseModel):
    """
    Class responsible for the `posts` table in the PostgreSQL DB
    """

    email: EmailStr
    password: str

    class Config:
        """
        Class responsible for compatibility between SQLAlchemy schemas and Pydantic models.
        """

        orm_mode = True
