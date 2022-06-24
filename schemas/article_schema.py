from pydantic import BaseModel, HttpUrl
from typing import Optional


class ArticleSchema(BaseModel):
    id: Optional[int]
    title: str
    description: str
    root_url: HttpUrl
    user_id: Optional[int]
    # creator = relationship() NÂO TEM

    class Config:
        orm_mode = True
