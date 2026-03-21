from sqlalchemy.orm import relationship
from app import db, bcrypt
from .basemodel import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    places = relationship('Place', backref='user', lazy=True)

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def __init__(self, first_name, last_name, email, password, admin=False):
        super().__init__()
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip().lower()
        self.password = self.hash_password(password)
        self.is_admin = admin


"""
IN REPO User
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
"""
