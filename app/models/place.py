from app.models.basemodel import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)

    def remove_review(self, review):
        self.reviews.remove(review)

    def update_review(self, review):
        self.remove_review(review)
        self.add_review(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        self.amenities.remove(amenity)

    def update_amenity(self, amenity):
        self.remove_amenity(amenity)
        self.add_amenity(amenity)
