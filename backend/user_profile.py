from fastapi import APIRouter,Depends,Security
#from app.schema import ResponseSchema, RegisterSchema, LoginSchema, ForgotPasswordSchema
from jwt_auth import get_current_active_user
from models import User
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials
#from app.service.users import UserService

router = APIRouter(
    prefix="/users",
    tags=['Profile']
)

@router.get("/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user