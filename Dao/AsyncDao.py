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

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from asyncpg import Pool
from asyncpg.pool import PoolConnectionProxy
from contextlib import asynccontextmanager

class AsyncDao[T](ABC):

    def __init__(self, pool: Pool) -> None:
        self.pool = pool

    @asynccontextmanager
    async def acquire(self) -> AsyncGenerator[PoolConnectionProxy, None]:
        async with self.pool.acquire() as pconn:
            yield pconn

    async def close(self):
        # 不由 DAO 關閉 pool
        raise NotImplementedError("Should not close the connection pool in DAO class")
    
    @abstractmethod
    async def getInfo(self, pconn: PoolConnectionProxy | None = None) -> T | None:
        pass
    
    @abstractmethod
    async def setInfo(self, key: str, value: str) -> bool:
        pass

    @abstractmethod
    async def pushNew(self, obj: T) -> bool:
        pass