from app.Index.app import app
import AsyncDao.AsyncItemDao
from pool import Pool # TODO

pool: Pool = #TODO
app.run(host="0.0.0.0", port=8000)