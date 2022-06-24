from typing import List, Optional

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from pydantic import EmailStr

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user_model import UserModel
from schemas.user_schema import UserSchemaBase, UserSchemaCreate, UserSchemaUpdate, UserSchemaArticles
from core.deps import get_session, get_current_user
from core.security import generate_hash_password
from core.auth import authenticate, create_access_token


router = APIRouter()


# GET LOGGED
@router.get('logged', response_model=UserSchemaBase)
def get_logged(logged_user: UserModel = Depends(get_current_user)):
    return logged_user


#POST / SIGN UP
@router.post('/sing_up', status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def post_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    new_user: UserModel = UserModel(
        name=user.name,
        lastname=user.lastname,
        email=user.email,
        password=generate_hash_password(user.password),
        is_admin=user.is_admin
    )
    async with db as session:
        session.add(new_user)
        await session.commit()

        return new_user


# GET USERS
@router.get('/', response_model=List[UserSchemaBase])
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users = result.scalars().unique().all()

        return users


#GET USER with your own articles
@router.get('/{user_id}', response_model=UserSchemaArticles, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user:
            return user
        else:
            raise HTTPException(detail='User not found.', status_code=status.HTTP_404_NOT_FOUND)


# PUT USER
@router.get('/{user_id}', response_model=UserSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_user(user_id: int, user: UserSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_update: UserModel = result.scalars().unique().one_or_none()

        if user_update:
            if user.name:
                user_update.name = user.name
            if user.lastname:
                user_update.lastname = user.lastname
            if user.email:
                user_update.email = user.email
            if user.is_admin:
                user_update.is_admin = user.is_admin
            if user.password:
                user_update.password = generate_hash_password(user.password)

            await session.commit()

            return user_update

        else:
            raise HTTPException(detail='User not found.', status_code=status.HTTP_404_NOT_FOUND)


# USER DELETE
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_del: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user_del:
            await session.delete(user_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='User not found.', status_code=status.HTTP_404_NOT_FOUND)


# POST LOGIN
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate(email=EmailStr(form_data.username), password=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid access data.')

    return JSONResponse(content={"access_token": create_access_token(sub=str(user.id)), "token_type": "bearer"},
    status_code=status.HTTP_200_OK)
