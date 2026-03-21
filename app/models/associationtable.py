from .basemodel import BaseModel
from app import db


class AssociationTable(BaseModel):
    __tablename__ = 'amenityplacemap'

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    amenity_id = db.Column(db.String(36), db.ForeignKey('amenities.id'), nullable=False)
