from sqlalchemy.orm import relationship
from .basemodel import BaseModel
from app import db


class Review(BaseModel):
	__tablename__ = 'reviews'

	text = db.Column(db.String(50), nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
	place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

	user = relationship('User', backref='user', lazy=True)
	place = relationship('Place', backref='place', lazy=True)

	def __init__(self, text, rating, place_id, user_id):
		super().__init__()
		self.text = text
		self.rating = rating
		self.place_id = place_id
		self.user_id = user_id


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
