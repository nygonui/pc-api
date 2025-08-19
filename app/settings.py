from decouple import config

from app.infra.database.config import ConnectionConfig, PoolConfig

# LOG_LEVEL = config(
#     "LOG_LEVEL",
#     default="info",
#     cast=Choices(["debug", "info", "warning", "error", "critical"], cast=str),
# )
LOCAL = config("LOCAL", default=False, cast=bool)
SERVER_HOST = str(config("SERVER_HOST", default="0.0.0.0", cast=str))
SERVER_PORT = config("SERVER_PORT", default=8000, cast=int)
WORKERS = config("WORKERS", default=5, cast=int)

DB_HOST = str(config("DB_HOST", default="localhost", cast=str))
DB_PORT = config("DB_PORT", default=5432, cast=int)
DB_NAME = str(config("DB_NAME", default="mydatabase", cast=str))
DB_USER = str(config("DB_USER", default="myuser", cast=str))
DB_PASSWORD = str(config("DB_PASSWORD", default="mypassword", cast=str))
DB_POOL_SIZE = config("DB_POOL_SIZE", default=3, cast=int)
DATABASE_CONFIG = ConnectionConfig(
    host=DB_HOST,
    port=DB_PORT,
    name=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    pool=PoolConfig(
        size=DB_POOL_SIZE,
    ),
)
