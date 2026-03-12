from asyncpg import Record
from asyncpg.pool import PoolConnectionProxy

from Dao.AsyncDao import AsyncDao
from Entity.Item import Item

class AsyncItemDao(AsyncDao[Item]):

    item_type: str
    item_id: str

    def __init__(self, type: str = "_", id: str = "_"):
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

    async def getItemsAutomatically(self, count: int = 8, pconn: PoolConnectionProxy[Record] | None = None):
        query = "select * from getItems($1, $2)"
        if pconn:
            async for row in pconn.cursor(query, self.item_type if self.item_type != "_" else "null", count):
                yield row
        async with self.acquire() as pconn_tmp:
            async for row in pconn_tmp.cursor(query, self.item_type if self.item_type != "_" else "null", count):
                yield row
    