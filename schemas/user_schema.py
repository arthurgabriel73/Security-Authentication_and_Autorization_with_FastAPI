from typing import List

from pydantic import BaseModel, EmailStr
from schemas.article_schema import ArticleSchema


class UserSchemaBase(BaseModel):
    id: int | None = None
    name: str | None = None
    lastname: str | None = None
    email = EmailStr
    # password = str NÂO TEM
    is_admin: bool = False
    # articles = relationship() NÂO TEM

    class Config:
        orm_mode = True


class UserSchemaCreate(UserSchemaBase):
    password: str


class UserSchemaArticles(UserSchemaBase):
    articles: List[ArticleSchema] | None


class UserSchemaUpdate(UserSchemaBase):
    name: str | None
    lastname: str | None
    email: EmailStr | None
    password: str | None
    is_admin: bool | None
