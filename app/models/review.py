from app import db, bcrypt
from .basemodel import BaseModel


class Review(BaseModel):
	__tablename__ = 'reviews'

	text = db.Column(db.String(50), nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
	place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)


"""
# IN REPO
class Review(BaseModel):
	def __init__(self, text, rating, place, user):
		super().__init__()
		self.text = text
		self.rating = rating
		self.place = place
		self.user = user
"""
