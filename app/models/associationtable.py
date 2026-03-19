from .basemodel import BaseModel
#from app import db
from .associationtable import AssociationTable


class AssociationTable(BaseModel):
    __tablename__ = 'amenityplacemap'

    place_id = db.Column(db.String(36), ForeignKey('places.id'), nullable=False)
    amenity_id = db.Column(db.String(36), ForeignKey('amenities.id'), nullable=False)
