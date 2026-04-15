from app.domain.models import User
from app.domain.repositories import UserRepository
from app.domain.exceptions import UserNotFound, UserAlreadyExists
from app.security.password_hasher import hash_password


class UserDomainService:

    def __init__(self, repository: UserRepository):
        self.repository = repository


    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)
        return user


    def get_user_by_email(self, email: str) -> User:
        user = self.repository.get_by_email(email)
        if user is None:
            raise UserNotFound(email)
        return user


    def create_user(self, email: str, password_hash: str, role: str) -> User:
        if self.repository.get_by_email(email) is not None:
            raise UserAlreadyExists(email)
        user = User(
            email = email,
            password_hash = hash_password(password_hash),
            role = role,
            is_active = True,   # dominio o service define estado inicial
        )
        self.repository.save(user)
        return user


    def update_user(self, user_id: int, is_active: bool, role: str) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFound(user_id)
        user.is_active = is_active
        user.role = role
        self.repository.update(user)
        return user
