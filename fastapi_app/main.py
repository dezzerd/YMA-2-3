from fastapi import FastAPI
from database import database, engine, metadata
from crud import create_user as crud_create_user, get_users as crud_get_users
import schemas

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/users/", response_model=schemas.User)
async def create_user_endpoint(user: schemas.UserCreate):
    return await crud_create_user(user)

@app.get("/users/", response_model=list[schemas.User])
async def read_users_endpoint():
    return await crud_get_users()
