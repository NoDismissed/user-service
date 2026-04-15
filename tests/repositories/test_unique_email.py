import pytest
from sqlalchemy.exc import IntegrityError
from app.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from app.domain.models import User


def test_unique_email_constraint(db_session):
    repo = SqlAlchemyUserRepository(db_session)
    user1 = User(
        email = "unique@test.com",
        password_hash = "hash",
        role = "user",
    )
    user2 = User(
        email = "unique@test.com",
        password_hash = "hash2",
        role = "user",
    )
    repo.save(user1)
    with pytest.raises(IntegrityError):
        repo.save(user2)
