from datetime import datetime, timezone
from uuid import uuid4


from app.domain.entities.user import User
from app.domain.ports.user_repository import UserRepository
from app.domain.ports.password_hasher import PasswordHasher
from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId
from app.use_cases.dtos.register_user import RegisterUserRequest, RegisterUserResponse
from app.domain.entities.auth_credentials import AuthCredentials
from app.domain.ports.auth_repository import AuthRepository


class RegisterUser:
    def __init__(
        self,
        user_repo: UserRepository,
        auth_repo: AuthRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._user_repo = user_repo
        self._auth_repo = auth_repo
        self._hasher = password_hasher

    async def execute(self, req: RegisterUserRequest) -> RegisterUserResponse:
        email = Email(req.email)

        existing = await self._user_repo.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")

        user = User(
            id=UserId(uuid4()),
            email=email,
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )

        # Todavía no guardamos credenciales (lo haremos en el siguiente paso con AuthCredentials)
        # Por ahora el hasher queda listo para la parte de login/registro real
        password_hash = self._hasher.hash(req.password)

        await self._user_repo.create(user)

        credentials = AuthCredentials(
            user_id=user.id,
            password_hash=password_hash,
            provider="local",
        )

        await self._auth_repo.create(credentials)

        return RegisterUserResponse(user_id=str(user.id.value), email=user.email.value)
