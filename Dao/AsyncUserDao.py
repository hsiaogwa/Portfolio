from Dao.AsyncDao import AsyncDao
from quart import Blueprint, request, jsonify, current_app
from asyncpg import Connection, Pool, Record
from datetime import datetime, timedelta

user_bp = Blueprint('user', __name__, url_prefix='/user')

class UserDao(AsyncDao):

	__isLogged: bool = False
	uid: str
	_recordInfo: Record | None = None
	

	def __init__(self, id: str):
		super().__init__()
		self.uid = id

	"""
	# 舊版的UserDao，使用同步的psycopg2進行操作
	@deprecated.deprecated(reason="Use asyncpg version getInfoPsy instead", version="2.0.0")
	def getInfo(self):
		if self.__isLogged:
			self.cur.execute("SELECT id, country, email, description, name, headp, gender, age, birthday, theme FROM users WHERE id = %s", (self.uid,))
			return self.cur.fetchone()
		else:
			self.cur.execute("SELECT id, description, name, headp, gender, age, birthday, theme FROM users WHERE id = %s", (self.uid,))
			return self.cur.fetchone()

	# 重構後的UserDao，使用asyncpg進行異步操作
	# 用戶DAO類，支持異步數據庫操作
	async def getInfoPsy(self):
		async with self.pool.acquire() as conn:
			if self.__isLogged:
				query = "SELECT id, country, email, description, name, headp, gender, age, birthday, theme FROM users WHERE id = $1"
			else:
				query = "SELECT id, description, name, headp, gender, age, birthday, theme FROM users WHERE id = $1"
			return await conn.fetchrow(query, self.uid)
	"""

	async def getInfo(self):
		if self._recordInfo is not None:
			return self._recordInfo
		else:
			async with self.pool.acquire() as conn:
				query = "SELECT id, country, email, description, name, headp, gender, age, birthday, theme FROM users WHERE id = $1"
				row = await conn.fetchrow(query, self.uid)
				self._recordInfo = row
				return row

	async def setInfo(self, data):
		# TODO
		pass

	async def check_ip_login(self, ip: str):
		async with self.pool().acquire() as conn:
			query = """
				SELECT logdate FROM main.userip
				WHERE userid = $1 AND logip = $2 AND logout = FALSE
				ORDER BY logdate DESC LIMIT 2
			"""
			row = await conn.fetchrow(query, self.uid, ip)
			if row:
				last_login = row['logdate']
				if last_login > datetime.now() - timedelta(days=30):
					self.__isLogged = True
					return True
			return False

	async def record_ip_login(self, ip: str):
		async with self.pool.acquire() as conn:
			query = """
				INSERT INTO main.userip (userid, logip, logdate)
				VALUES ($1, $2, $3)
			"""
			await conn.execute(query, self.uid, ip, datetime.now())

	async def invalidate_ip_login(self, ip: str):
		async with self.pool.acquire() as conn:
			query = """
				UPDATE main.userip
				SET logout = TRUE
				WHERE userid = $1 AND logip = $2 AND logout = FALSE
			"""
			await conn.execute(query, self.uid, ip)

	async def login(self, password: str, ip: str):
		# 檢查IP是否在30天內登錄過
		if await self.check_ip_login(ip):
			info = await self.getInfo()
			return {"statement": 1, "description": "Auto login by IP", "data": dict(info) if info else None}
		# 密碼登錄流程
		async with self.pool.acquire() as conn:
			query = "SELECT password FROM users WHERE id = $1"
			res = await conn.fetchrow(query, self.uid)
			if not res:
				return {"statement": 4, "description": "User not exist"}
			elif res['password'] != password:
				return {"statement": 3, "description": "Password error"}
			else:
				self.__isLogged = True
				await self.record_ip_login(ip)
				info = await self.getInfo()
				return {"statement": 1, "description": "Login success", "data": dict(info) if info else None}

# Blueprint路由，調用方法如下：
# POST /user/login { "uid": "...", "password": "...", "ip": "..." }
@user_bp.route('/login', methods=['POST'])
async def login():
	data = await request.get_json()
	uid = data.get('uid')
	password = data.get('password')
	ip = data.get('ip', request.remote_addr)
	pool = current_app.config['DB_POOL']
	user_dao = UserDao(uid, pool)
	result = await user_dao.login(password, ip)
	return jsonify(result)

# 安全關閉方法：用戶在輸入密碼步驟離開時，前端可調用 /user/logout
@user_bp.route('/logout', methods=['POST'])
async def logout():
	# 此處可根據session或token進行登出處理
	return jsonify({"statement": 2, "description": "Logout success"})