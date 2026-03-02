from app.models.basemodel import BaseModel

class Review(BaseModel):
	def __init__(self, text, rating, place, user):
		super().__init__()
		self.text = text
		self.rating = rating
		self.place = place
		self.user = user

	def create_review(self, review_data):
		# Logic to create a review, including validation for user_id, place_id, and rating
		#  check if required information is provided
		required_keys = ['text', 'rating', 'place', 'user']
		for key in required_keys:
			if key not in review_data:
				raise ValueError(f"Missing required field: {key}")
			
		#  check if rating is in required range of 1 - 5
		if not (1 <= review_data['rating'] <= 5):
			raise ValueError("Rating must be between 1 and 5")

		#  create new review
		review = Review(
			text=review_data['text'],
			rating=review_data['rating'],
			place=review_data['place'],
			user=review_data['user']
		)

		# save review
		review.save()

		return review
	

	def get_review(self, review_id):
		# Logic to retrieve a review by ID
		for review in Review.get_all(): # correct function??
			if review.id == review_id:
				return review
		return None
	

	def get_all_reviews(self):
		# Logic to retrieve all reviews
		return Review.get_all()


	def get_reviews_by_place(self, place_id):
		# Logic to retrieve all reviews for a specific place
		return [review for review in Review.get_all() if review.place.id == place_id]


	def update_review(self, review_id, review_data):
		# Logic to update a review
		review = self.get_review(review_id) # fetch review
		if not review:
			return None #  or do we need an error?
		
		if 'text' in review_data: #  option to update part of review
			review.text = review_data['text']
		if 'rating' in review_data:
			if not (1 <= review_data['rating'] <= 5): #  check if rating is in range
				raise ValueError("Rating must be between 1 and 5")
			review.rating = review_data['rating']
			
		review.save()
		return review


	def delete_review(self, review_id):
		# Logic to delete a review
		review = self.get_review(review_id) #  fetch review
		if not review:
			return None #  or do we have to raise error?
		review.delete()
		return review
