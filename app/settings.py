from decouple import config

# LOG_LEVEL = config(
#     "LOG_LEVEL",
#     default="info",
#     cast=Choices(["debug", "info", "warning", "error", "critical"], cast=str),
# )
LOCAL = config("LOCAL", default=False, cast=bool)
SERVER_HOST = str(config("SERVER_HOST", default="0.0.0.0", cast=str))
SERVER_PORT = config("SERVER_PORT", default=8000, cast=int)
WORKERS = config("WORKERS", default=5, cast=int)
