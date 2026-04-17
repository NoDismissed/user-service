class DomainError(Exception):
    # clase base para todos los errores de dominio
    pass


class UserNotFound(DomainError):
    def __init__(self, user_id: int):
        super().__init__(f"User with id {user_id} not found")
        self.user_id = user_id


class UserAlreadyExists(DomainError):
    def __init__(self, email: str):
        super().__init__(f"User with email {email} already exists")
        self.email = email


class InvalidCredentials(DomainError):
    def __init__(self):
        super().__init__("Invalid email or password")


class UserInactive(DomainError):
    def __init__(self):
        super().__init__("User inactive")
