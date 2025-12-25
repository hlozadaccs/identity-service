from uuid import UUID

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UserId:
    value: UUID
