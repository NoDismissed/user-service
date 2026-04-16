import grpc
import pytest
from app.grpc import auth_pb2, user_pb2


def test_authenticate_success(grpc_stub_auth, grpc_stub_user):
    created = grpc_stub_user.CreateUser(
        user_pb2.CreateUserRequest(
            email = "auth@test.com",
            password_hash = "secret",
            role = "user",
        )
    )
    response = grpc_stub_auth.Authenticate(
        auth_pb2.AuthenticateRequest(
            email = "auth@test.com",
            password = "secret",
        )
    )
    assert response.id == created.id
    assert response.role == "user"


def test_authenticate_invalid_password(grpc_stub_auth, grpc_stub_user):
    grpc_stub_user.CreateUser(
        user_pb2.CreateUserRequest(
            email = "auth2@test.com",
            password_hash = "secret",
            role = "user",
        )
    )
    with pytest.raises(grpc.RpcError) as exc:
        grpc_stub_auth.Authenticate(
            auth_pb2.AuthenticateRequest(
                email = "auth2@test.com",
                password = "wrong",
            )
        )
    assert exc.value.code() == grpc.StatusCode.UNAUTHENTICATED
