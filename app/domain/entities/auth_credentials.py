from dataclasses import dataclass
from app.domain.value_objects.user_id import UserId


@dataclass(slots=True)
class AuthCredentials:
    user_id: UserId
    password_hash: str
    provider: str  # "local", "google", etc.
