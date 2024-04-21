from fastapi import APIRouter
from models import CreateUserRequest, UserInDB
from fastapi import FastAPI, HTTPException, Body, status, Depends
from jwt_auth import pwd_context, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, SECRET_KEY, ALGORITHM
from connection import userdb
from models import *
from pymongo import ReturnDocument
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="/auth", tags=['Authentication'])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model = None)
async def create_user(create_user_request: User):
    create_user_model = User(
        username=create_user_request.username,
        password=pwd_context.hash(create_user_request.password),
        email=create_user_request.email
    )

    new_user = userdb.insert_one(
        create_user_model.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = userdb.find_one(
        {"_id": new_user.inserted_id}
    )

    created_user['_id'] = str(created_user['_id'])
    return created_user


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(userdb, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/forgot-password", status_code=status.HTTP_201_CREATED, response_model = None)
async def update_password(updated_user: ForgotPasswordSchema):
    
    hashed_password=pwd_context.hash(updated_user.password)
    

    update_user = userdb.find_one_and_update(
        {'email' : updated_user.email},
        {'$set' : { "password" : hashed_password }},
        return_document= ReturnDocument.AFTER
    )

    if update_user:
        return {"message": "Password updated successfully"}
    else:
        return {"message": "User not found or password not updated"}

#extra endpoints will follow