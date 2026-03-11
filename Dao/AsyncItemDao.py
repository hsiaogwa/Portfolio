from asyncpg import Pool, Record

from Dao.AsyncDao import AsyncDao
from asyncpg.pool import PoolConnectionProxy

class ItemDao(AsyncDao):

	item_type: str
	item_id: str

	def __init__(self, type: str = "", id: str = ""):
		super().__init__()
		self.item_type = type
		self.item_id = id

	async def getInfo(self, pconn: PoolConnectionProxy[Record] | None = None):
		query = "select itype, id, title from Item where itype = $1 and id = $2"
		if pconn:
			return await pconn.fetchrow(query, self.item_type, self.item_id)
		async with self.acquire() as pconn_tmp:
			return await pconn_tmp.fetchrow(query, self.item_type, self.item_id)

	async def setInfo(self, key, value):
		# TODO
		pass
	