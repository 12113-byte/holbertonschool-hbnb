from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        pass

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
    
