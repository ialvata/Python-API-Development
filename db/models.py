from database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean, default=True)
    # created_at = Column(TIMESTAMP)
