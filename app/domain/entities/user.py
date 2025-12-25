from dataclasses import dataclass
from datetime import datetime

from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId


@dataclass(slots=True)
class User:
    id: UserId
    email: Email
    is_active: bool
    created_at: datetime
