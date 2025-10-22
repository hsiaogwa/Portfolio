from Dao.AsyncDao import AsyncDao

async def ASN_INIT_PACKAGE_DAO_SYSFUNC():
	await AsyncDao.init_pool()

from Dao.AsyncDao import AsyncDao