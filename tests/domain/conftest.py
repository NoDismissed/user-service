import pytest
from app.domain.repositories import UserRepository


class InMemoryUserRepository(UserRepository):

    def __init__(self):
        self.users = {}
        self._next_id = 1


    def get_by_id(self, user_id: int):
        return self.users.get(user_id)


    def get_by_email(self, email: str):
        return next(
            (u for u in self.users.values() if u.email == email),
            None,
        )


    def save(self, user):
        if user.id is None:
            user.id = self._next_id
            self._next_id += 1
        self.users[user.id] = user


    def update(self, user):
        if user.id in self.users:
            self.users[user.id] = user


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()
