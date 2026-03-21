import hashlib
from app.models.basemodel import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, admin=False):
        super().__init__()
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip().lower()
        self.password = self._hash_password(password)
        self.is_admin = admin

    def _hash_password(self, password):
        #swap this it flask_bycrypt
        return hashlib.sha256(password.encode()).hexdigest()

