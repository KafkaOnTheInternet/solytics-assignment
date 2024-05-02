from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class User(BaseModel):
    _id: str
    name: str
    hashed_password: str

@app.post('/create_user/')
async def create_user(user: User):
    return {'user': user}

@app.get('/read_user/{user_id}')
async def read_user(user_id: int, request: Request):
    headers = request.headers
    cookies = request.cookies

    return {'user_id': user_id, 'headers': headers, 'cookies': cookies}
