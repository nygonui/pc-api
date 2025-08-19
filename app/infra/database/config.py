from dataclasses import dataclass

from escudeiro.misc import lazymethod
from escudeiro.url import URL, Netloc
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

    @lazymethod
    def make_uri(self, *, is_asyncio: bool) -> URL:
        """Create a database URI."""
        scheme = "postgresql+asyncpg" if is_asyncio else "postgresql+psycopg"
        return URL.from_args(
            netloc_obj=Netloc.from_args(
                host=self.connection.host,
                port=self.connection.port,
                username=self.connection.user,
                password=self.connection.password,
            ),
            scheme=scheme,
            path=self.connection.name,
        )
