from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, data):
        existing = self.user_repo.find_by("email", data.get("email", "").strip().lower())
        if existing:
            raise ValueError("A user with this email already exists.")
        user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            password=data.get("password"),
            admin=data.get("admin", False)
        )
        return self.user_repo.save(user)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def update_user(self, uid, user_data):
        user = self.user_repo.get(uid)
        if not user:
            return None
        if "first_name" in user_data and user_data["first_name"]:
            user.first_name = user_data["first_name"].strip()
        if "last_name" in user_data and user_data["last_name"]:
            user.last_name = user_data["last_name"].strip()
        if "email" in user_data and user_data["email"]:
            existing = self.user_repo.find_by("email", user_data["email"].strip().lower())
            if existing and existing.uid != uid:
                raise ValueError("A user with this email already exists.")
            user.email = user_data["email"].strip().lower()
        if "password" in user_data and user_data["password"]:
            user.password = user._hash_password(user_data["password"])
        return self.user_repo.update(user)

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        return self.place_repo.get(place_id)
        
facade = HBnBFacade()
