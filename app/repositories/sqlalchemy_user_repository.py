from sqlalchemy.orm import Session
from app.domain.models import User
from app.domain.repositories import UserRepository
from app.db.models import UserModel


class SqlAlchemyUserRepository(UserRepository):

    def __init__(self, db: Session):
        self.db = db


    def get_by_id(self, user_id: int) -> User | None:
        model = self.db.get(UserModel, user_id)
        return self._to_domain(model) if model else None


    def get_by_email(self, email: str) -> User | None:
        model = (
            self.db.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )
        return self._to_domain(model) if model else None


    def save(self, user: User) -> None:
        model = UserModel(
            email = user.email,
            password_hash = user.password_hash,
            role = user.role,
            is_active = user.is_active,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        user.id = model.id


    def update(self, user: User) -> None:
        model = self.db.get(UserModel, user.id)
        model.is_active = user.is_active
        model.role = user.role
        self.db.commit()


    def _to_domain(self, model: UserModel) -> User:
        return User(
            id = model.id,
            email = model.email,
            password_hash = model.password_hash,
            role = model.role,
            is_active = model.is_active,
        )
