import os


# no usa .env, seguro en todos los entornos
ENV = os.getenv("ENV", "local")
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")
