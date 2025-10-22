from Dao.AsyncDao import Dao

class ItemDao(Dao):

	item_type: str
	item_selector: str

	def __init__(self, type: str = "", selector: str = ""):
		super().__init__()
		self.item_type = type
		self.item_selector = selector

	def getInfo(self):
		# TODO: Implement item retrieval logic based on type and selector