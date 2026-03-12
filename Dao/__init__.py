from warnings import deprecated

from Dao.AsyncDao import AsyncDao
from Dao.AsyncItemDao import AsyncItemDao
from Dao.AsyncUserDao import AsyncUserDao

@deprecated("No behaviors in modern version now.\nDAO will self-init automatically when instantiated.")
async def ASN_INIT_PACKAGE_DAO_SYSFUNC():
    pass