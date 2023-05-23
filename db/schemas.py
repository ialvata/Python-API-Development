"""
Module responsible for pydantic schemas
"""
# pylint: disable = too-few-public-methods
from typing import Optional

from pydantic import BaseModel


class Post(BaseModel):
    """
    Class docstring
    """

    title: str
    content: str | None = None
    published: bool = True
    rating: Optional[int] = None

    # class Config:
    #     orm_mode = True
