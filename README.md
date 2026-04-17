# User Service

Microservicio que gestiona el ciclo de vida de usuarios con DB propia y se expone via gRPC

- flask, framework para aplicaciones web, flexible, minimalista
- microservicio, estilo de arquitectura donde las responsabilidades se dividen independientemente
- un microservicio es dueño de su BD, ningun otro puede leer o escribir
- entre BDs en comun, las tablas no estan relacionadas solo tienen identificadores pero sin llaves foraneas
- grpc (google remote procedure call), marco de trabajo para conectar servicios, muy rapido y ligero, protobuf
- grpc es un adaptador pero no dominio
- niveles de scope en fixtures ( session > package > module > class > function )
- chmod +x docker/entrypoint.sh, permisos de ejecucion (change mode) +x añadir o execute

- flask http expone el sistema
- grpc para comunicacion entre servicios y solo a sus respectivas BDs
- no se comparten las BDs
- api gateway (flask http) no tiene BD
- cada servicio es unidad autonoma y se despliega independiente
- capas internas de cada microservicio
- rutas flask > capa grpc > casos de uso > capa dominio (negocio) > capa repositorio > postgres
- se empieza con dominio + tests de dominio, despues infraestructura
- al agregar frozen al decorador @dataclass, transforma la clase en no mutable solo lectura
- @abstractmethod metodo debe implementarse por clase hija (clase abstracta no se instancia solo hijas)
- db.merge en sqlalchemy, sobreescribe si ID ya existe, crea copia vinculada original sigue fuera, se usa para
  reincorporar datos que venian de cache, api o sesion cerrada
- forzar registro de tablas en alembic env.py
- ejecutar alembic upgrade head para local y tests al cambiar de variables de entorno para una nueva migracion
- se reemplazo .toml por requirements.txt por problemas con incompatibilidad
- tests de repositorio validan atomicidad por eso se usa rollback
- tests de grpc validan flujo completo sin atomicidad, no se usa rollback
- se tiene que hacer import relativo explicito en los archivos pb2_grpc.py (from .)
- cuando hay migracion sin cambios reales, alembic aun se queda con la version anterior y es correcto
- en render, crear primero la BD

- pip install -e .[dev], -e es editable instala dependencias de toml, correr cada vez que se actualice
- set -a > source .env.local > set +a, exporta variables a shell
- alembic init alembic, crea la configuracion de alembic
- alembic revision --autogenerate -m "create users table", crea migracion
- alembic upgrade head, genera la migracion en la BD
- alembic current, muestra el head de alembic
- pytest tests/repositories, ejecutar pruebas en directorio especifico
- docker compose down
- docker compose up --build
- docker compose build --no-cache
- docker compose ps, muestra detalle de contenedores
- python -m pip install -r requirements-dev.txt, mejor ejecucion
- python -m grpc_tools.protoc \
  -I app/grpc/proto \
  --python_out=app/grpc \
  --grpc_python_out=app/grpc \
  app/grpc/proto/*.proto
  (crea stubs en carpeta destino)
- docker exec -it user-service python, entrar al contenedor del servicio
- docker exec -it microservice-user-db psql -U finance -d microservice_user, entrar al contenedor de postgres
- pytest.ini para ejecutar de raiz los tests en estructura app

- \d table_name, muestra detalle de tabla