import pytest
from app.db.session import engine, SessionLocal


@pytest.fixture(scope = "session")
def db_engine():
    return engine


@pytest.fixture(scope = "function")
def db_session(db_engine):
    # crea nueva sesion de BD por test envuelto en una transaccion que se revierte
    connection = db_engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind = connection)
    yield session
    transaction.rollback()
    session.close()
    connection.close()
