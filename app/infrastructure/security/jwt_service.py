from datetime import datetime, timedelta, timezone

import jwt


class JwtService:
    def __init__(self, secret: str, expires_minutes: int = 15) -> None:
        self._secret = secret
        self._expires = expires_minutes

    def create_access_token(self, subject: str) -> str:
        payload = {
            "sub": str(subject),
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=self._expires),
            "iat": datetime.now(tz=timezone.utc),
        }
        return jwt.encode(payload, self._secret, algorithm="HS256")
