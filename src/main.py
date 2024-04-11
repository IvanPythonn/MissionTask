from random import randint
from typing import Union, List
from fastapi import FastAPI
from schemas import CreateUser, ReadUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User
from database import engine
app = FastAPI(title="Центр документов", description='Самый важный центр документов')

users = {}


@app.get('/')
async def hello():
    return {"Hello": "World"}


@app.get('/user')
async def get_users(offset:int, limit: int) -> List[ReadUser]:
    async with AsyncSession(engine) as session:
        stmt = select(User).offset(offset).limit(limit)
        users = await session.scalars(stmt)
        return users.all()

@app.get('/user/{user.id}')
async def get_one_user(user_id: int) -> ReadUser:
    async with AsyncSession(engine) as session:
        stmt = select(User).where(User.id==user_id)
        user = await session.scalars(stmt)
        return user.first()

@app.post('/user')
async def add_user(user: CreateUser):
    stmt = User(name=user.name, fullname=user.fullname, nickname=user.nickname)
    async with AsyncSession(engine) as session:
        session.add(stmt)
        await session.commit()
        await session.refresh(stmt)
        stmt2 = select(User).where(User.id == stmt.id)
        new_user = await session.scalars(stmt2)
        return new_user.first()

@app.delete("/user/{user.id}")
async def delete_user(user_id: int) -> dict:
    async with AsyncSession(engine) as session:
        stmt = select(User).where(User.id == user_id)
        user = await session.scalars(stmt)
        await session.delete(user)
        await session.commit()
    return {'Status': 'success',
            'detail': f"User {user_id} has been deleted"}

@app.patch('/user/{user.id}')
async def update_user(user_id: int, new_user: CreateUser) -> ReadUser:
    async with AsyncSession(engine) as session:
    stmt = select(User).where(User.id==user_id)
    result = await session.scalars(stmt)
    user: User = result.first()
    user.name= new_user.name
    user.fullname = new_user.fullname
    user.nickname = new_user.nickname
    session.add(user)
    await session.commit()
    stmt = select(User).where(User.id == user_id)
    result = await session.scalars(stmt)
    return result.first()
