from abc import ABC, abstractmethod
from asyncpg import create_pool, Pool
from asyncio import Lock

class AsyncDao(ABC):
	_pool:Pool | None = None
	_initLock : Lock | None = None

	@classmethod
	async def _init_pool(cls):
		if cls._pool is None:
			if cls._initLock is None:
				cls._initLock = Lock()		# Singleton pattern
			async with cls._initLock:
				if cls._pool is None:
					cls._pool = await create_pool(
						user='postgres',
						password='vul3xu.3ck6al3',
						database='main',
						host='127.0.0.1',
						port=5432,
						min_size=3,
						max_size=15
					)
					if cls._pool is None:
						raise Exception("Failed to create database connection pool")				
		return cls._pool
	
	def __init__(self):
		if self._pool is None:
			raise Exception("Database connection pool is not initialized. Call AsyncDao.init_pool() before using.")
		self.pool = self._pool

	@property
	async def pool(self) -> Pool:
		if self.__class__._pool is None:
			await self.__class__._init_pool()
		return self.__class__._pool

	def close(cls):
		if cls._pool is not None:
			cls._pool.close()
			cls._pool = None

	async def __del__(self):
		self.close()

	@abstractmethod
	async def getInfo(self):
		pass

	@abstractmethod
	async def setInfo(self, data):
		pass