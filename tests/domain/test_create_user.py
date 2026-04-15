import pytest
from app.domain.services.user import UserDomainService
from app.domain.exceptions import UserAlreadyExists


def test_create_user_success(user_repository):
    service = UserDomainService(user_repository)
    user = service.create_user(
        email = "new@test.com",
        password_hash = "hash",
        role = "user",
    )
    assert user.is_active is True
    assert user.email == "new@test.com"


def test_create_user_duplicate_email(user_repository):
    service = UserDomainService(user_repository)
    service.create_user(
        email = "dup@test.com",
        password_hash = "hash",
        role = "user",
    )
    with pytest.raises(UserAlreadyExists):
        service.create_user(
            email = "dup@test.com",
            password_hash = "hash",
            role = "user",
        )
