from fastapi import APIRouter
from fastapi.responses import JSONResponse

from utils.jwt_manager import create_token
from schemas.auth import User

auth_router = APIRouter()

@auth_router.post('/login', tags = ['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(content=token, status_code=200)