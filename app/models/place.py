from app import db, bcrypt
from sqlalchemy.orm import relationship
from .basemodel import BaseModel, AssociationTable

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(36), ForeignKey('users.id'), nullable=False)
    reviews = relationship('Review', backref='place', lazy=True)
    amenities = relationship('Amenity', secondary=AssociationTable, backref='place', lazy=True)

"""
# IN REPO
class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)

    def remove_review(self, review):
        self.reviews.remove(review)

    def update_review(self, review):
        self.remove_review(review)
        self.add_review(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        self.amenities.remove(amenity)

    def update_amenity(self, amenity):
        self.remove_amenity(amenity)
        self.add_amenity(amenity)
"""
