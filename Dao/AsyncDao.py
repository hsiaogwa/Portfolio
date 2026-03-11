"""classmethod
    async def _init_pool(cls) -> Pool:
        if cls._pool is None:
            if cls._initLock is None:
                cls._initLock = Lock()        # Singleton pattern
            async with cls._initLock:
                if cls._pool is None:
                    cls._pool = await create_pool(
                        user='postgres',
                        password='',
                        database='',
                        host='',
                        port=5432,
                        min_size=3,
                        max_size=15
                    )
                    if cls._pool is None:
                        raise Exception("Failed to create database connection pool")                
        return cls._pool
"""

from abc import ABC
from collections.abc import AsyncGenerator
from asyncio import Lock
from asyncpg import Pool
from asyncpg.pool import PoolConnectionProxy
from contextlib import asynccontextmanager

class AsyncDao(ABC):

    def __init__(self, pool: Pool) -> None:
        self.pool = pool
        self.__class__.__init_lock()

    @classmethod
    def __init_lock(cls):
        if not hasattr(cls, "_initLock"):
            cls._initLock = Lock()

    @asynccontextmanager
    async def acquire(self) -> AsyncGenerator[PoolConnectionProxy, None]:
        async with self.pool.acquire() as pconn:
            yield pconn

    async def close(self):
        # 不由 DAO 關閉 pool
        raise NotImplementedError("Should not close the connection pool in DAO class")