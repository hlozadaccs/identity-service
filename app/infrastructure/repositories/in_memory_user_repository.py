from app.domain.entities.user import User
from app.domain.ports.user_repository import UserRepository
from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._by_id: dict[str, User] = {}
        self._by_email: dict[str, User] = {}

    async def get_by_id(self, user_id: UserId) -> User | None:
        return self._by_id.get(str(user_id.value))

    async def get_by_email(self, email: Email) -> User | None:
        return self._by_email.get(email.value)

    async def create(self, user: User) -> None:
        self._by_id[str(user.id.value)] = user
        self._by_email[user.email.value] = user
