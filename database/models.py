from sqlalchemy import  Column, String, Integer

from .database import Base


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)

