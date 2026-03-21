from app import db
from .basemodel import BaseModel
from .associationtable import AssociationTable


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    #places = relationship('Place', secondary=AssociationTable.__table__)

"""
# IN REPO
class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name
"""
