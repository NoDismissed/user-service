import pytest
from app.domain.services.user import UserDomainService
from app.domain.models import User
from app.domain.exceptions import UserNotFound


def test_get_user_success(user_repository):
    user = User(
        email = "test@test.com",
        password_hash = "x",
        role = "user"
    )
    user_repository.save(user)
    service = UserDomainService(user_repository)
    result = service.get_user(user.id)
    assert result.email == "test@test.com"
    assert result.is_active is True


def test_get_user_not_found(user_repository):
    service = UserDomainService(user_repository)
    with pytest.raises(UserNotFound):
        service.get_user(999)
