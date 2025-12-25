from app.domain.value_objects.email import Email
from app.domain.ports.user_repository import UserRepository
from app.domain.ports.auth_repository import AuthRepository
from app.domain.ports.password_hasher import PasswordHasher
from app.use_cases.dtos.login_user import LoginUserRequest, LoginUserResponse


class LoginUser:
    def __init__(
        self,
        user_repo: UserRepository,
        auth_repo: AuthRepository,
        password_hasher: PasswordHasher,
        token_service,
    ) -> None:
        self._user_repo = user_repo
        self._auth_repo = auth_repo
        self._hasher = password_hasher
        self._token_service = token_service

    async def execute(self, req: LoginUserRequest) -> LoginUserResponse:
        email = Email(req.email)

        user = await self._user_repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")

        credentials = await self._auth_repo.get_by_user_id(user.id)
        if not credentials:
            raise ValueError("Invalid credentials")

        if not self._hasher.verify(req.password, credentials.password_hash):
            raise ValueError("Invalid credentials")

        token = self._token_service.create_access_token(
            subject=user.id.value
        )

        return LoginUserResponse(access_token=token)
