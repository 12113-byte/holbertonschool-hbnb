from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity

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
        # Logic will be implemented in later tasks
        pass


    def create_amenity(self, amenity_data):
    # check if requirements are met to create amenity
        if "name" not in amenity_data: #  check if amenity has name
            raise ValueError("Amenity name is missing.")
        
        extracted_name = amenity_data.get("name") #  extracting name from data

        if not isinstance(extracted_name, str): #  check if extracted name is a str
            raise ValueError("Amenity name must be a string.")

        if extracted_name.strip() == "": #  check if extracted name is empty
            raise ValueError("Amenity name cannot be empty.")
        
        new_amenity = Amenity(name=extracted_name) #  create new amenity
        self.amenity_repo.add(new_amenity) #  save new amenity to repo
        return new_amenity


    def get_amenity(self, amenity_id):
    # Logic to retrieve an amenity by ID
        if not isinstance(amenity_id, str): # check if amenity exists and is a str
            raise ValueError("Amenity ID must be a string.")
        
        amenity = self.amenity_repo.get_by_attribute("id", amenity_id) #  fetch from repo

        if amenity is None: #  if not found, return None
            return None
        #  or raise error
        #  reutrn ValueError("Amenity not found")
        

    def get_all_amenities(self):
    # Logic to retrieve all amenities
        amenities = self.amenity_repo.get_all()
        return amenities


    def update_amenity(self, amenity_id, amenity_data):
    # Logic to update an amenity
    
        if not isinstance(amenity_id, str): #  check if amenity_id exists and is a str
            raise ValueError("Amenity ID must be a string.")
        
        amenities = self.amenity_repo.get_by_attribute("id", amenity_id) # fetch amenity from repo

        if not amenities: #  empty list if not found
            return None
        
        amenity = amenities[0]

        if "name" not in amenity_data: #  check if new name in amenity_data
            raise ValueError("Amenity name is missing.")
        
        extracted_name = amenity_data["name"] #  extract name

        if not isinstance(extracted_name, str): #  check if exists and is a str
            raise ValueError("Amenity must be a string.")

        if extracted_name.strip() == "": #  check if extracted name is empty
            raise ValueError("Amenity name cannot be empty.")
        
        amenity.name = extracted_name #  update fields
        self.amenity_repo.update(amenity) #  save changes

        return amenity
    
