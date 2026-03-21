from app import db, bcrypt
from .basemodel import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # relationships
    places = db.relationship('Place', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    # relationships

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
    def __init__(self, first_name, last_name, email, admin=False):
        super().__init__()

        
        # Basic validation is done here 
        # -------------------------------
        if not first_name:
            raise ValueError("First name is required.")
        if not last_name:
            raise ValueError("Last name is required.")
        if not email:
            raise ValueError("Email is required.")
        if not self._validate_email(email):
            raise ValueError("Invalid email format.")

      
        # Assign attributes are assigned here
        # -------------------------------
        
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip().lower()

        # Password will be stored hashed instead of plain text as we had before
        self.password = None

        self.is_admin = admin

<<<<<<< HEAD
 
    # Email validation helping mechanism 
    # -------------------------------
    def _validate_email(self, email):
        #Validate email format using regex.
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    
    # Actual meat Password hashing using bcrypt
    # -------------------------------
    def hash_password(self, password):
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long.")

        # Generate hash and decode to string for storage
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

   
    # Password verification
    # -------------------------------
    
    def verify_password(self, password):
        if not self.password:
            return False

        return bcrypt.check_password_hash(self.password, password)

   
    # Safe serialization process
    # -------------------------------
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }


##
    __tablename__ = "users"

    # Columns (Database fields)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    # Unique email 
    email = db.Column(db.String(120), nullable=False, unique=True)

    # Store hashed password ONLY
    password = db.Column(db.String(128), nullable=False)

    is_admin = db.Column(db.Boolean, default=False)

    
    # Email validation
    def validate_email(self):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, self.email):
            raise ValueError("Invalid email format.")

    # Password hashing
    def hash_password(self, password):
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long.")

        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Password verification
    def verify_password(self, password):
    
        return bcrypt.check_password_hash(self.password, password)

    # Safe response 
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }
    
=======
    def _hash_password(self, password):
        #swap this it flask_bycrypt
        return hashlib.sha256(password.encode()).hexdigest()
"""
>>>>>>> Max
