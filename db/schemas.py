# pylint: disable = too-few-public-methods
"""
Module responsible for the document/table models to exist in the PostgreSQL DB
"""
from sqlalchemy import TIMESTAMP, Boolean, Column, Float, Integer, String
from sqlalchemy.sql.expression import text

from db.db_orm import Base


class Post(Base):
    """
    Class responsible for the `posts` table in the PostgreSQL DB
    """

    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean, server_default="TRUE")
    rating = Column(Float, server_default="0")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class User(Base):
    """
    Class responsible for the `posts` table in the PostgreSQL DB
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
