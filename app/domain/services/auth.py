from app.security.password_hasher import verify_password
from app.domain.exceptions import InvalidCredentials


class UserDomainService:

    def __init__(self, repo):
        self.repo = repo


    def authenticate(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user:
            raise InvalidCredentials()
        if not verify_password(password, user.password_hash):
            raise InvalidCredentials()
        return user
