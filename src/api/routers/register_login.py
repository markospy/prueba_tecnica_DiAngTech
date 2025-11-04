from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.api.routers.user_router import get_use_cases_user
from src.api.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from src.schemas.security import Token
from src.schemas.user import UserIn, UserOut
from src.services.use_cases_user import UseCasesUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


app_security = APIRouter(tags=["register and login"])


@app_security.post("/register/", response_model=UserOut)
async def create_user(
    user: UserIn,
    use_cases_user: UseCasesUser = Depends(get_use_cases_user),
):
    return await use_cases_user.create_user(user)


@app_security.post("/login/", response_model=Token)
async def authenticate_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    use_cases_user: UseCasesUser = Depends(get_use_cases_user),
):
    user = await use_cases_user.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")
