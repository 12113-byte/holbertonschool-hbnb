#from app.persistence.repository import InMemoryRepository #might need to remove this
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository #new sqlalchemy repo
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
import re


class HBnBFacade:
    def __init__(self):

        # Replace in-memory repo with SQLAlchemy repo
        self.user_repo = SQLAlchemyRepository(User)

        
        #self.user_repo = InMemoryRepository()
        #self.place_repo = InMemoryRepository()
        #self.review_repo = InMemoryRepository()
        #self.amenity_repo = InMemoryRepository()

    """
        Users
    """

def create_user(self, user_data):
    

        # Create User object
        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"]
        )

        # Hash password before saving (IMPORTANT)
        user.hash_password(user_data["password"])

        # Save to database
        self.user_repo.add(user)

        return user

    # Get User by ID
    # -------------------------------
    def get_user(self, user_id):
        
        #Retrieve a user by ID.
        return self.user_repo.get(user_id)

    
    # Get all users
    def get_all_users(self):
        return self.user_repo.get_all()

    
    
   """ # Create a new User
    def create_user(self, user_data):
        b, m = self.string_validation(user_data['first_name'], "first_name", 50)
        if (b is False):
            raise Exception(m)
        b, m = self.string_validation(user_data['last_name'], "last_name", 50)
        if (b is False):
            raise Exception(m)
        b, m = self.email_validation(user_data['email'])
        if (b is False):
            raise Exception(m)

        user = User(**user_data)
        self.user_repo.add(user)
        return user

    # Get user by User uuid
    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    # Get user by User email
    def get_user_by_email(self, email):
        b, m = self.email_validation(email)
        if (b is False):
            raise Exception(m)
        return self.user_repo.get_by_attribute("email", email)

    def update_user(self, user_id, user_data):
        b, m = self.string_validation(user_data['first_name'], "first_name", 50)
        if (b is False):
            raise Exception(m)
        b, m = self.string_validation(user_data['last_name'], "last_name", 50)
        if (b is False):
            raise Exception(m)
        b, m = self.email_validation(user_data['email'])
        if (b is False):
            raise Exception(m)

        return self.user_repo.update(user_id, user_data)

   """
    """
        Places
    """
    # Create a new place
    def create_place(self, place_data):
        b, m = self.string_validation(place_data['title'], "title", 100)
        if (b is False):
            raise Exception(m)
        b, m = self.price_validation(place_data['price'])
        if (b is False):
            raise Exception(m)

        b, m = self.latitude_validation(place_data['latitude'])
        if (b is False):
            raise Exception(m)

        b, m = self.longitude_validation(place_data['longitude'])
        if (b is False):
            raise Exception(m)

        get_user = self.user_repo.get(place_data['owner_id'])
        if get_user is None:
            raise Exception("User not found")

        place = Place(place_data['title'], place_data['description'], place_data['price'], place_data['latitude'], place_data['longitude'], get_user)
        self.place_repo.add(place)
        return place

    # Get place by place id
    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    # return all places in the memory repo
    def get_all_places(self):
        return self.place_repo.get_all()

    # update a place's data
    def update_place(self, place_id, place_data):
        b, m = self.string_validation(place_data['title'], "title", 100)
        if (b is False):
            raise Exception(m)
        b, m = self.price_validation(place_data['price'])
        if (b is False):
            raise Exception(m)

        b, m = self.latitude_validation(place_data['latitude'])
        if (b is False):
            raise Exception(m)

        b, m = self.longitude_validation(place_data['longitude'])
        if (b is False):
            raise Exception(m)

        return self.place_repo.update(place_id, place_data)

    """
        Amenities
    """
    def create_amenity(self, amenity_data):
        b, m = self.string_validation(amenity_data['name'], "name", 50)
        if (b is False):
            raise Exception(m)

        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        b, m = self.string_validation(amenity_data['name'], "name", 50)
        if (b is False):
            raise Exception(m)
        return self.amenity_repo.update(amenity_id, amenity_data)

    """
        Review
    """
    def create_review(self, review_data):
        #Checking that user is associated with the review exists
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise Exception("User not found")

        #Checking that place is associated with the review exists
        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise Exception("Place not found")

        #Checking review text is not empty or missing
        if not review_data['text']:
            raise Exception("Review text is required")
        
        #Ensuring rating is an integer between 1 and 5
        rating = review_data['rating']
        if not (1 <= rating <= 5):
            raise Exception("Rating must be between 1 and 5")

        review = Review(review_data['text'], review_data['rating'], place, user)
        self.review_repo.add(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        # r for reviews
        return [r for r in self.review_repo.get_all() if r.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        #save updated review back to repository
        return self.review_repo.update(review_id, review)

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        # Verifies the review exists before attempt
        review = self.review_repo.get(review_id)
        if not review:
            raise Exception("review not found") #review not found
        
        place = self.place_repo.get(review.place.id)
        place.remove_review(review)
        return self.review_repo.delete(review_id)

    """
        Validation Methods
    """
    def string_validation(self, string, input_name, length):
        if isinstance(string, str) is False:
            return False, f"{input_name} must be a string"

        if len(string) == 0:
            return False, f"{input_name} cannot be empty"

        if len(string) > length:
            return False, f"{input_name} cannot be greater than {length}"

        return True, "success"

    def sring_no_max_validation(self, string, input_name):
        if isinstance(string, str) is False:
            return False, f"{input_name} must be a string"

        if len(string) == 0:
            return False, f"{input_name} cannot be empty"

        return True

    def email_validation(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email) is not None:
            return True, "success"

        return False, "invalid email address"

    def price_validation(self, price):
        if isinstance(price, (float, int)) is False:
            return False, "price must be a positive number"

        if price < 1:
            return False, "price must be a positive number"

        return True, "success"

    def latitude_validation(self, latitude):
        if isinstance(latitude, (float, int)) is False:
            return False, "latitude must be a number"

        if latitude < -90 or latitude > 90:
            return False, "latitude must be valid (between -90 and 90)"

        return True, "success"

    def longitude_validation(self, longitude):
        if isinstance(longitude, (float, int)) is False:
            return False, "longitude must be a number"

        if longitude < -180 or longitude > 180:
            return False, "longitude must be valid (between -180 and 180)"

        return True, "success"
