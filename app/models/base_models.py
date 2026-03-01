import uuid
from datetime import datetime

class BaseModel:
    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.creation_datetime = datetime.utcnow()
        self.last_update_datetime = datetime.utcnow()

    def save(self):
        self.last_update_datetime = datetime.utcnow()   

    def to_dict(self):
        return {
            "id": self.id,
            "creation_datetime": self.creation_datetime.isoformat(),
            "last_update_datetime": self.last_update_datetime.isoformat()
        }
