from app.models.basemodel import BaseModel

class Amenity(BaseModel):
	def __init__(self, name):
		super().__init__()
		if len(name) == 0:
			raise ValueError("Name cannot be Empty")
		self.name = name
