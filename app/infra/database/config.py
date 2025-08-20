from dataclasses import dataclass
from urllib.parse import quote_plus

from pydantic import BaseModel, Field


class PoolConfig(BaseModel):
    size: int = 10
    max_overflow: int = 5
    recycle: int = 3600


class ConnectionConfig(BaseModel):
    host: str
    user: str
    password: str
    name: str
    port: int = 5432
    pool: PoolConfig = Field(default_factory=PoolConfig)


@dataclass
class DatabaseConfig:
    connection: ConnectionConfig

    def make_uri(self, *, is_asyncio: bool) -> str:
        """Create a database URI."""
        scheme = "postgresql+asyncpg" if is_asyncio else "postgresql+psycopg"
        user = quote_plus(self.connection.user)
        password = quote_plus(self.connection.password)
        return f"{scheme}://{user}:{password}@{self.connection.host}:{self.connection.port}/{self.connection.name}"
