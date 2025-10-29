import datetime

class Item:
	import datetime

class Item:

	__slots__ = ['id', '_type', '_data', '_date']

	id: str
	@property
	def type(self) -> str:
		return self._type
	@type.setter
	def type(self, value: str):
		if not isinstance(value, str):
			raise TypeError("type 必须是 str")
		self._type = value
	@property
	def data(self) -> dict:
		return self._data
	@data.setter
	def data(self, value: dict):
		if not isinstance(value, dict):
			raise TypeError("data 必须是 dict")
		self._data = value
	@property
	def date(self) -> datetime.datetime:
		return self._date
	@date.setter
	def date(self, value: datetime.datetime):
		if not isinstance(value, datetime.datetime):
			raise TypeError("date 必须是 datetime.datetime")
		self._date = value

	def __init__(self, id: str, type: str, data: dict, date: datetime):
		self.id, self._type, self._data, self._date = id, type, data, date
		return self