from app.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from app.domain.models import User


def test_save_and_get_user(db_session):
    repo = SqlAlchemyUserRepository(db_session)
    user = User(
        email = "repo@test.com",
        password_hash = "hash",
        role = "user",
    )
    repo.save(user)
    fetched = repo.get_by_email("repo@test.com")
    assert fetched is not None
    assert fetched.email == "repo@test.com"
    assert fetched.role == "user"
    assert fetched.is_active is True


def test_get_by_email(db_session):
    repo = SqlAlchemyUserRepository(db_session)
    user = User(
        email = "email@test.com",
        password_hash = "hash",
        role = "admin",
    )
    repo.save(user)
    fetched = repo.get_by_email("email@test.com")
    assert fetched is not None
    assert fetched.email == "email@test.com"
