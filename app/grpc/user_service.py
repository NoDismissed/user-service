import grpc
from app.grpc import user_pb2, user_pb2_grpc
from app.domain.services.user import UserDomainService
from app.domain.exceptions import UserNotFound, UserAlreadyExists
from app.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from app.db.session import SessionLocal


class UserGrpcService(user_pb2_grpc.UserServiceServicer):

    # adaptador: traduce llamadas gRPC a casos de uso del dominio
    def _get_service(self):
        db = SessionLocal()
        repo = SqlAlchemyUserRepository(db)
        service = UserDomainService(repo)
        return db, service


    def GetUser(self, request, context):
        db, service = self._get_service()
        try:
            user = service.get_user(request.id)
            return user_pb2.UserResponse(
                id = user.id,
                email = user.email,
                role = user.role,
                is_active = user.is_active,
            )
        except UserNotFound:
            context.abort(grpc.StatusCode.NOT_FOUND, "USER_NOT_FOUND")
        finally:
            db.close()


    def CreateUser(self, request, context):
        db, service = self._get_service()
        try:
            user = service.create_user(
                email = request.email,
                password_hash = request.password_hash,
                role = request.role,
            )
            return user_pb2.UserResponse(
                id = user.id,
                email = user.email,
                role = user.role,
                is_active = user.is_active,
            )
        except UserAlreadyExists:
            context.abort(grpc.StatusCode.ALREADY_EXISTS, "USER_ALREADY_EXISTS")
        finally:
            db.close()


    def UpdateUser(self, request, context):
        db, service = self._get_service()
        try:
            user = service.update_user(
                user_id = request.id,
                is_active = request.is_active,
                role = request.role,
            )
            return user_pb2.UserResponse(
                id = user.id,
                email = user.email,
                role = user.role,
                is_active = user.is_active,
            )
        except UserNotFound:
            context.abort(grpc.StatusCode.NOT_FOUND,"USER_NOT_FOUND")
        finally:
            db.close()
