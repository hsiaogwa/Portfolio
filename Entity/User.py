from datetime import date
import json

class User:
	from datetime import date

class User:
	__slots__ = ['_id', '_country', '_email', '_description', '_name', '_headp', '_gender', '_age', '_birthday', '_theme']

	FIELD_TYPES = {
		'id': str,
		'country': str,
		'email': str,
		'description': str,
		'name': str,
		'headp': str,
		'gender': int,
		'age': str,
		'birthday': date,
		'theme': dict,
	}

	def __init__(self, **kwargs):
		for key, value in kwargs.items():
			if key not in self.FIELD_TYPES:
				raise ValueError(f"无效字段: {key}")
			setattr(self, key, value)

	@property
	def id(self) -> str:
		"""GET: 返回私有字段 _id"""
		return self._id

	@property
	def country(self) -> str:
		return self._country

	@country.setter
	def country(self, value: str):
		if not isinstance(value, str):
			raise TypeError("country 必须是 str")
		if len(value) != 2:
			raise ValueError("country 必须是 2 字符")
		self._country = value

	@property
	def email(self) -> str:
		return self._email

	@email.setter
	def email(self, value: str):
		if not isinstance(value, str):
			raise TypeError("email 必须是 str")
		if len(value) > 100:
			raise ValueError("email 最长 100 字符")
		# email 格式验证
		self._email = value

	@property
	def gender(self) -> int:
		return self._gender

	@gender.setter
	def gender(self, value: int):
		if not isinstance(value, int):
			raise TypeError("gender 必须是 int")
		if value not in (0, 1, 2, 3, 4):
			raise ValueError("gender 必须是 0, 1, 2, 3, 4")
		self._gender = value

	@property
	def birthday(self) -> date:
		return self._birthday

	@birthday.setter
	def birthday(self, value: str | date):
		if isinstance(value, str):
			try:
				value = date.fromisoformat(value)  # 支持 '2025-01-01'
			except ValueError:
				raise ValueError("birthday 格式错误，应为 YYYY-MM-DD")
		elif not isinstance(value, date):
			raise TypeError("birthday 必须是 date 或 ISO 格式字符串")
		self._birthday = value

	@property
	def theme(self) -> dict:
		return self._theme

	@theme.setter
	def theme(self, value: str | dict):
		if isinstance(value, str):
			try:
				value = json.loads(value)
			except json.JSONDecodeError:
				raise ValueError("theme JSON 格式错误")
		elif not isinstance(value, dict):
			raise TypeError("theme 必须是 dict 或 JSON 字符串")
		self._theme = value
	
	@property
	def description(self) -> str:
		return self._description
	
	@description.setter
	def description(self, value: str):
		if not isinstance(value, str):
			raise TypeError("description 必须是 str")
		if len(value) > 300:
			raise ValueError("description 最长 400 字符")
		self._description = value

	@property
	def name(self) -> str:
		return self._name
	
	@name.setter
	def name(self, value: str):
		if not isinstance(value, str):
			raise TypeError("name 必须是 str")
		if len(value) > 30:
			raise ValueError("name 最长 20 字符")
		self._name = value

	@property
	def headp(self) -> str:
		return self._headp
	
	@headp.setter
	def headp(self, value: str):
		if not isinstance(value, str):
			raise TypeError("headp 必须是 str")
		self._headp = value

	@property
	def age(self) -> str:
		return self._age
	
	@age.setter
	def age(self, value: str):
		if not isinstance(value, str):
			raise TypeError("age 必须是 str")
		if len(value) > 4:
			raise ValueError("age 最长 4 字符")
		self._age = value