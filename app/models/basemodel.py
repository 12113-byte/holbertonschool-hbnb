from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True;

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AssociationTable(BaseModel):
    __tablename__ = 'amenityplacemap'

    place_id = db.Column(db.String(36), ForeignKey('places.id'), nullable=False)
    amenity_id = db.Column(db.String(36), ForeignKey('amenities.id'), nullable=False)

"""
-- BaseModel from part 2 (In memory repo)
class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
"""
