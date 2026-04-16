import grpc
from app.grpc import auth_pb2_grpc, auth_pb2, auth_pb2_grpc
from app.domain.services.auth import AuthDomainService
from app.domain.exceptions import InvalidCredentials
from app.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from app.db.session import SessionLocal


class AuthGrpcService(auth_pb2_grpc.AuthServiceServicer):

    # adaptador: traduce llamadas gRPC a casos de uso del dominio
    def _get_service(self):
        db = SessionLocal()
        repo = SqlAlchemyUserRepository(db)
        service = AuthDomainService(repo)
        return db, service


    def Authenticate(self, request, context):
        db, service = self._get_service()
        try:
            user = service.authenticate(
                email = request.email,
                password = request.password,
            )
            return auth_pb2.AuthenticateResponse(
                id = user.id,
                role = user.role,
            )
        except InvalidCredentials:
            context.abort(grpc.StatusCode.UNAUTHENTICATED,"INVALID_CREDENTIALS")
        finally:
            db.close()
