from decouple import Choices, config

LOCAL = config("LOCAL", default=False, cast=bool)
LOG_LEVEL = config(
    "LOG_LEVEL",
    default="info",
    cast=Choices(["debug", "info", "warning", "error", "critical"], cast=str),
)
SERVER_HOST = str(config("SERVER_HOST", default="0.0.0.0", cast=str))
SERVER_PORT = config("SERVER_PORT", default=8000, cast=int)
