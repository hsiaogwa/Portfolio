from asyncpg import Pool, Record
from asyncpg.pool import PoolConnectionProxy

from Dao.AsyncDao import AsyncDao
from Entity.User import User

class AsyncUserDao(AsyncDao[User]):

    uid: str
    
    def __init__(self, id: str, pool: Pool) -> None:
        super().__init__(pool)
        self.uid = id

    async def getInfo(self, pconn:PoolConnectionProxy[Record] | None = None) -> Record | None:
        query = "call getPersonInfo($1)"
        if pconn:
            return await pconn.fetchrow(query, self.uid)
        async with self.acquire() as pconn_tmp:
            return await pconn_tmp.fetchrow(query, self.uid)

    async def setInfo(self, key, value) -> bool:
        # TODO
        pass

    async def check_ip_login(self, ip: str, pconn:PoolConnectionProxy[Record] | None = None) -> bool:
        """
        Check if the IP has logged in within 30 days
        @param ip: e.g. '123.45.0.0/20'
        @return: bool - whether the IP has logged successfully
        """
        query = "select * from checkLogin($1, $2)"
        if pconn:
            row = await pconn.fetchrow(query, self.uid, ip)
        else:
            async with self.acquire() as pconn_tmp:
                row = await pconn_tmp.fetchrow(query, self.uid, ip)
        if row:
            return row['checking']
        return False

    async def record_ip_login(self, ip: str, pconn:PoolConnectionProxy[Record] | None = None) -> None:
        query = "call loginIp($1, $2)"
        if pconn:
            await pconn.execute(query, self.uid, ip)
        else:
            async with self.acquire() as pconn_tmp:
                await pconn_tmp.execute(query, self.uid, ip)
        return None

    async def invalidate_ip_login(self, ip: str, pconn:PoolConnectionProxy[Record] | None = None) -> None:
        query = """
            UPDATE main.userip
            SET logout = true
            WHERE userid = $1 AND logip = $2 AND logout = false
        """
        if pconn:
            await pconn.execute(query, self.uid, ip)
        else:
            async with self.acquire() as pconn_tmp:
                await pconn_tmp.execute(query, self.uid, ip)
        return None

    async def login(self, password: str | None, ip: str) -> dict:
        async with self.acquire() as pconn:
            # 檢查IP是否在30天內登錄過
            if self.check_ip_login(ip, pconn):
                return {"statement": 2, "description": "Login success with IP fast login", "data": "__cached__"}
            # 密碼登錄流程
            query = "select * from checkLogin($1, $2, $3)"
            res = await pconn.fetchrow(query, self.uid, ip, password)
            if not res:
                return {"statement": 4, "description": "User not exist"}
            elif res['checking'] is False:
                return {"statement": 1, "description": "Password incorrect"}
            elif res['checking'] is True:
                await self.record_ip_login(ip, pconn)
                return {"statement": 2, "description": "Login success", "data": dict(await self.getInfo())}