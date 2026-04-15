from abc import ABC, abstractmethod
from app.domain.models import User


class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        pass


    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass


    @abstractmethod
    def save(self, user: User) -> None:
        pass
