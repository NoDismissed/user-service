from concurrent import futures
import grpc
from app.grpc.user_service import UserGrpcService
from app.grpc.auth_service import AuthGrpcService
from app.grpc import user_pb2_grpc
from app.grpc import auth_pb2_grpc


def serve():
    # configura el servidor gRPC, esta funcion debe ser importable para pruebas
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
    user_pb2_grpc.add_UserServiceServicer_to_server(
        UserGrpcService(), server
    )
    auth_pb2_grpc.add_AuthServiceServicer_to_server(
        AuthGrpcService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("User gRPC Service running on port 50051")
    print("Auth gRPC Service running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
