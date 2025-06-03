from fastapi import HTTPException
from database import database
from models import users
from schemas import UserCreate

async def get_user_by_email(email: str):
    return await database.fetch_one(users.select().where(users.c.email == email))

async def create_user(user: UserCreate):
    if await get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")  # Добавлен отступ

    query = users.insert().values(name=user.name, email=user.email)
    user_id = await database.execute(query)
    return await get_user(user_id)

async def get_users():
    return await database.fetch_all(users.select())


async def get_user(user_id: int):
    user = await database.fetch_one(users.select().where(users.c.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")  # Добавлен отступ
    return dict(user)