import hashlib
import re
from app.models.basemodel import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, admin=False):
        super().__init__()
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip().lower()
        #self.password = self._hash_password(password)
        self.is_admin = admin

    def _validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
