from dataclasses import dataclass
from typing import Optional


@dataclass
class UserContext:
    user_id: str
    role: str


def parse_bearer_token(token: Optional[str]) -> Optional[UserContext]:
    # Placeholder for future JWT/OAuth integration.
    if not token:
        return None
    return UserContext(user_id='anonymous', role='viewer')