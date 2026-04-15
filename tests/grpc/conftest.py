import pytest
import threading
import time
import grpc
from app.grpc.server import serve
from app.db.session import engine
from app.db.base import Base
from app.grpc import user_pb2_grpc


@pytest.fixture(scope = "session", autouse = True)
def prepare_database():
    # asegurarse de que BD exista para pruebas gRPC, alembic ya corrio migraciones, esto es una red de seguridad
    Base.metadata.create_all(bind = engine)
    yield


@pytest.fixture(scope = "session")
def grpc_server():
    thread = threading.Thread(target = serve, daemon = True)
    thread.start()
    time.sleep(1)
    yield
    # sin necesidad de hacer nada, el servidor gRPC se ejecuta en un hilo separado y se cerrara automaticamente al finalizar las pruebas


@pytest.fixture
def grpc_stub(grpc_server):
    channel = grpc.insecure_channel("localhost:50051")
    return user_pb2_grpc.UserServiceStub(channel)
