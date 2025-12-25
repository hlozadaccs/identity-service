from abc import ABC, abstractmethod

from app.domain.entities.auth_credentials import AuthCredentials
from app.domain.value_objects.user_id import UserId


class AuthRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: UserId) -> AuthCredentials | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, credentials: AuthCredentials) -> None:
        raise NotImplementedError
