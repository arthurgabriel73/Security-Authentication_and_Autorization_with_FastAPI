from pydantic import BaseModel, HttpUrl


class ArticleSchema(BaseModel):
    id: int | None = None
    title: str
    description: str
    root_url: HttpUrl
    user_id: int | None = None
    # creator = relationship() NÂO TEM


class Config:
    orm_mode = True
