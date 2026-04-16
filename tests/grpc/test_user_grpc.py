import grpc
import pytest
from app.grpc import user_pb2


def test_create_and_get_user(grpc_stub_user):
    response = grpc_stub_user.CreateUser(
        user_pb2.CreateUserRequest(
            email = "grpc_user@test.com",
            password_hash = "hash",
            role = "user",
        )
    )
    assert response.email == "grpc_user@test.com"
    assert response.role == "user"
    assert response.is_active is True
    fetched = grpc_stub_user.GetUserByEmail(
        user_pb2.GetUserByEmailRequest(email = "grpc_user@test.com")
    )
    assert fetched.email == "grpc_user@test.com"


def test_create_user_duplicate_email(grpc_stub_user):
    grpc_stub_user.CreateUser(
        user_pb2.CreateUserRequest(
            email = "duplicate@test.com",
            password_hash = "hash",
            role = "user",
        )
    )
    with pytest.raises(grpc.RpcError) as exc:
        grpc_stub_user.CreateUser(
            user_pb2.CreateUserRequest(
                email = "duplicate@test.com",
                password_hash = "hash",
                role = "user",
            )
        )
    assert exc.value.code() == grpc.StatusCode.ALREADY_EXISTS


def test_get_user_not_found(grpc_stub_user):
    with pytest.raises(grpc.RpcError) as exc:
        grpc_stub_user.GetUser(
            user_pb2.GetUserRequest(id = 999)
        )
    assert exc.value.code() == grpc.StatusCode.NOT_FOUND


def test_disable_user(grpc_stub_user):
    grpc_stub_user.CreateUser(
        user_pb2.CreateUserRequest(
            email = "disable@test.com",
            password_hash = "hash",
            role = "user",
        )
    )
    fetched = grpc_stub_user.GetUserByEmail(
        user_pb2.GetUserByEmailRequest(email = "disable@test.com")
    )
    grpc_stub_user.UpdateUser(
        user_pb2.UpdateUserRequest(
            id = fetched.id,
            is_active = False,
            role = "user"
        )
    )
    disabled = grpc_stub_user.GetUser(
        user_pb2.GetUserRequest(id = fetched.id)
    )
    assert disabled.is_active is False
