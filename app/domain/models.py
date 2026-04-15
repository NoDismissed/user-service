from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    email: str
    password_hash: str
    role: str
    is_active: bool = True
    id: Optional[int] = None
