import hashlib
import re
from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, admin=False):
        super().__init__()

        if not first_name:
            raise ValueError("First name is required.")
        if not last_name:
            raise ValueError("Last name is required.")
        if not email:
            raise ValueError("Email is required.")
        if not self._validate_email(email):
            raise ValueError("Invalid email format.")
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip().lower()
        self.password = self._hash_password(password)
        self.admin = admin

    def _validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "admin": self.admin
    })
        return base
