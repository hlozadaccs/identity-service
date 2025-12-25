from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from app.infrastructure.repositories.in_memory_user_repository import InMemoryUserRepository
from app.infrastructure.repositories.in_memory_auth_repository import InMemoryAuthRepository
from app.infrastructure.security.bcrypt_hasher import BcryptPasswordHasher
from app.infrastructure.security.jwt_service import JwtService
from app.use_cases.commands.register_user import RegisterUser
from app.use_cases.commands.login_user import LoginUser
from app.use_cases.dtos.register_user import RegisterUserRequest
from app.use_cases.dtos.login_user import LoginUserRequest


router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterBody(BaseModel):
    email: EmailStr
    password: str


class LoginBody(BaseModel):
    email: EmailStr
    password: str


_user_repo = InMemoryUserRepository()
_hasher = BcryptPasswordHasher()

_auth_repo = InMemoryAuthRepository()
_jwt_service = JwtService(secret="dev-secret")


def get_register_uc() -> RegisterUser:
    return RegisterUser(
        user_repo=_user_repo,
        auth_repo=_auth_repo,
        password_hasher=_hasher,
    )


def get_login_uc() -> LoginUser:
    return LoginUser(
        user_repo=_user_repo,
        auth_repo=_auth_repo,
        password_hasher=_hasher,
        token_service=_jwt_service,
    )


@router.post("/register", status_code=201)
async def register(body: RegisterBody, uc: RegisterUser = Depends(get_register_uc)):
    try:
        res = await uc.execute(RegisterUserRequest(email=str(body.email), password=body.password))
        return asdict(res)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(body: LoginBody, uc: LoginUser = Depends(get_login_uc),):
    uc = LoginUser(
        user_repo=_user_repo,
        auth_repo=_auth_repo,
        password_hasher=_hasher,
        token_service=_jwt_service,
    )
    try:
        res = await uc.execute(
            LoginUserRequest(
                email=str(body.email),
                password=body.password,
            )
        )
        return asdict(res)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
