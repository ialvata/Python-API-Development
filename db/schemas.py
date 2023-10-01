# pylint: disable = too-few-public-methods
"""
Module responsible for the document/table models to exist in the PostgreSQL DB
"""
from __future__ import annotations

import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import text

# from typing import List


# from db.db_orm import Base


class Base(DeclarativeBase):
    """
    The default map type mapping, deriving the type for mapped_column(),
    from a Mapped[] annotation, is:
    type_map: Dict[Type[Any], TypeEngine[Any]] = {
        bool: types.Boolean(),
        bytes: types.LargeBinary(),
        datetime.date: types.Date(),
        datetime.datetime: types.DateTime(),
        datetime.time: types.Time(),
        datetime.timedelta: types.Interval(),
        decimal.Decimal: types.Numeric(),
        float: types.Float(),
        int: types.Integer(),
        str: types.String(),
        uuid.UUID: types.Uuid(),
    }
    More info at
    https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
    """

    type_annotation_map = {
        datetime.datetime: TIMESTAMP(timezone=True),
    }


class Post(Base):
    """
    Class responsible for the `posts` table in the PostgreSQL DB
    """

    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(
        ForeignKey("users_table.username", ondelete="CASCADE")
    )
    user: Mapped["User"] = relationship(back_populates="posts")
    # To establish a bidirectional relationship in one-to-many,
    # where the “reverse” side is a many to one, we must specify an additional relationship()
    # in Post table and connect the two using the relationship.back_populates parameter,
    # and using the attribute name of each relationship() as the value for
    # relationship.back_populates on the other
    title: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    published: Mapped[bool] = mapped_column(server_default="TRUE")
    rating: Mapped[float] = mapped_column(server_default="0")
    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, server_default=text("now()")
    )

    def __repr__(self) -> str:
        return f"Post(id = {self.id}, username = {self.username})"


class User(Base):
    """
    Class responsible for the `users_table` table in the PostgreSQL DB
    """

    __tablename__ = "users_table"
    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, server_default=text("now()")
    )


class Vote(Base):
    __tablename__ = "votes"
    username: Mapped[str] = mapped_column(
        ForeignKey("users_table.username", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users_table.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )
    published: Mapped[bool] = mapped_column(server_default="TRUE")
    rating: Mapped[float] = mapped_column(server_default="0")
