from typing import List

from pydantic import BaseModel


class Article(BaseModel):
    id: str
    title: str
    description: str

    class Config:
        orm_mode = True

class ArticleList(BaseModel):
    id: List[str]
    title: List[str]

    class Config: 
        orm_mode = True

