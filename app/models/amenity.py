from app import db
from .basemodel import BaseModel
from .associationtable import AssociationTable


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
