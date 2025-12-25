from abc import ABC, abstractmethod

from app.domain.entities.user import User
from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: Email) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, user: User) -> None:
        raise NotImplementedError
