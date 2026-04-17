from app.domain.services.user import UserDomainService
from app.domain.models import User


def test_disable_user(user_repository):
    user = User(
        email = "a@test.com",
        password_hash = "x",
        role = "user",
    )
    user_repository.save(user)
    service = UserDomainService(user_repository)
    service.update_user(
        user_id = user.id,
        is_active = False,
        role = "user"
    )
    updated = user_repository.get_by_id(user.id)
    assert updated.is_active is False
