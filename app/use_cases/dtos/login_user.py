from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LoginUserRequest:
    email: str
    password: str

@dataclass(frozen=True, slots=True)
class LoginUserResponse:
    access_token: str
    token_type: str = "bearer"
