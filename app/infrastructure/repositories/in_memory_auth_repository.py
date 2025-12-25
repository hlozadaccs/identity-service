from app.domain.entities.auth_credentials import AuthCredentials
from app.domain.ports.auth_repository import AuthRepository
from app.domain.value_objects.user_id import UserId


class InMemoryAuthRepository(AuthRepository):
    def __init__(self) -> None:
        self._by_user_id: dict[str, AuthCredentials] = {}

    async def get_by_user_id(self, user_id: UserId) -> AuthCredentials | None:
        return self._by_user_id.get(user_id.value)

    async def create(self, credentials: AuthCredentials) -> None:
        self._by_user_id[credentials.user_id.value] = credentials
