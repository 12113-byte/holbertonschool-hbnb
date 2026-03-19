from app import db, bcrypt
from sqlalchemy.orm import relationship
from .basemodel import BaseModel, AssociationTable


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    text = db.Column(db.String(50), nullable=False)
    places = relationship('Place', secondary=AssociationTable, backref='amenity')

"""
# IN REPO
class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
"""
