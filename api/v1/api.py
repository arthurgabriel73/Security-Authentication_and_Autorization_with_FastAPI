from fastapi import APIRouter
from api.v1.endpoints import articles, users


api_router = APIRouter()

api_router.include_router(articles.router, prefix='/articles', tags=['articles'])
api_router.include_router(users.router, prefix='/users', tags=['users'])

