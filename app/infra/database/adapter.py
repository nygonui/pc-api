from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from functools import cached_property
from typing import Any, cast

import sqlalchemy as sa
import sqlalchemy.ext.asyncio as sa_async
from fastapi import Request

from .config import DatabaseConfig


@dataclass
class DatabaseAdapter:
    config: DatabaseConfig
    debug: bool = False

    @cached_property
    def engine(self) -> sa_async.AsyncEngine:
        return sa_async.create_async_engine(
            self.config.make_uri(is_asyncio=True),
            pool_size=self.config.connection.pool.size,
            echo=self.debug,
            pool_recycle=self.config.connection.pool.recycle,
            max_overflow=self.config.connection.pool.max_overflow,
        )

    async def new(self):
        return await self.engine.connect()

    async def is_closed(self, client: sa_async.AsyncConnection) -> bool:
        return client.closed

    async def release(self, client: sa_async.AsyncConnection) -> None:
        return await client.close()

    async def aclose(self) -> None:
        await self.engine.dispose()

    async def _do_with_transaction(
        self,
        client: sa_async.AsyncConnection,
        callback: Callable[[sa_async.AsyncTransaction], Awaitable[Any]],
    ) -> None:
        if not client.in_transaction():
            return
        trx = (
            client.get_transaction()
            if not client.in_nested_transaction()
            else client.get_nested_transaction()
        )
        if trx and trx.is_valid:
            await callback(trx)

    async def commit(self, client: sa_async.AsyncConnection) -> None:
        await self._do_with_transaction(
            client, sa_async.AsyncTransaction.commit
        )

    async def rollback(self, client: sa_async.AsyncConnection) -> None:
        await self._do_with_transaction(
            client, sa_async.AsyncTransaction.rollback
        )

    async def begin(self, client: sa_async.AsyncConnection) -> None:
        if not client.in_transaction():
            _ = await client.begin()
        else:
            _ = await client.begin_nested()

    async def in_atomic(self, client: sa_async.AsyncConnection) -> bool:
        """
        Check if the connection is in a transaction.
        """
        return client.in_transaction() or client.in_nested_transaction()

    @cached_property
    def session(self) -> "SessionAdapter":
        """
        Create a session adapter for the database connection.
        """
        return SessionAdapter(provider=self, debug=self.debug)


@dataclass
class SessionAdapter:
    """
    Session adapter for SQLAlchemy.
    """

    provider: DatabaseAdapter
    debug: bool = False

    async def new(self) -> sa_async.AsyncSession:
        """
        Create a new session.
        """
        return sa_async.AsyncSession(bind=await self.provider.new())

    def _get_bind(
        self, session: sa_async.AsyncSession
    ) -> sa_async.AsyncConnection:
        """
        Get the bind for the session.
        """
        return cast(sa_async.AsyncConnection, session.bind)

    async def is_closed(self, client: sa_async.AsyncSession) -> bool:
        """
        Check if the session is closed.
        """
        return self._get_bind(client).closed

    async def release(self, client: sa_async.AsyncSession) -> None:
        """
        Release the session.
        """
        await self._get_bind(client).close()

    async def aclose(self) -> None:
        """
        Close the session.
        """
        await self.provider.aclose()

    async def _do_with_transaction(
        self,
        client: sa_async.AsyncSession,
        callback: Callable[[sa_async.AsyncSessionTransaction], Awaitable[Any]],
    ) -> None:
        """
        Do something with the transaction.
        """
        if not client.in_transaction():
            return
        trx = (
            client.get_transaction()
            if not client.in_nested_transaction()
            else client.get_nested_transaction()
        )
        if trx:
            await callback(trx)

    async def commit(self, client: sa_async.AsyncSession) -> None:
        """
        Commit the session.
        """
        await self._do_with_transaction(
            client, sa_async.AsyncSessionTransaction.commit
        )

    async def rollback(self, client: sa_async.AsyncSession) -> None:
        """
        Rollback the session.
        """
        await self._do_with_transaction(
            client, sa_async.AsyncSessionTransaction.rollback
        )

    async def begin(self, client: sa_async.AsyncSession) -> None:
        """
        Begin the session.
        """
        if not client.in_transaction():
            _ = await client.begin()
        else:
            _ = await client.begin_nested()

    async def in_atomic(self, client: sa_async.AsyncSession) -> bool:
        """
        Check if the session is in a transaction.
        """
        return client.in_transaction() or client.in_nested_transaction()


# FastAPI Integration #

metadata = sa.MetaData()


async def create_session_adapter(
    provider: DatabaseAdapter,
) -> sa_async.AsyncSession:
    """
    Create a session adapter.
    """
    return await SessionAdapter(provider).new()


def get_session_adapter(request: Request) -> DatabaseAdapter:
    """
    Get the session adapter.
    """
    return request.app.state.session_adapter
