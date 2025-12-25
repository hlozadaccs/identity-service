from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegisterUserRequest:
    email: str
    password: str


@dataclass(frozen=True, slots=True)
class RegisterUserResponse:
    user_id: str
    email: str
