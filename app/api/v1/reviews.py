from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new reviews"""
        data = api.payload
        try:
            new_review = facade.create_review(data) #create review using facade method including validation
            return {"id": new_review.id, "rating": new_review.rating, "place": new_review.place.id, "user": new_review.user.id}, 201
        except Exception as e:
            return {"error": str(e)}, 400 # handles invalid input

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{
            "id": r.id,
            "text": r.text,
            "rating": r.rating,
            "user_id": r.user.id,
            "place_id": r.place.id
        } for r in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        # Placeholder for the logic to retrieve a review by ID
        review = facade.get_review(review_id) # Retrieve review using facade method

        #Returns 404 if review not found
        if not review:
            return {"error": "Review not found"}, 404
        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user.id,
            "place_id": review.place.id
        }, 200 #successful retrieval of review details

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        # Placeholder for the logic to update a review by ID
        data = api.payload
        # Attempt to update the review using the facade method
        review = facade.update_review(review_id, data)

        #return 404 if review not found
        if not review:
            return {"error": "Review not found"}, 404
        return {"message": "Review updated successfully"}, 200 #successful update of review

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        # Placeholder for the logic to delete a review
        try:
            facade.delete_review(review_id) # Attempt to delete the review using the facade method
        except Exception as e:
            return {"error": str(e)}, 400 # handles invalid input

        return {"message": "Review deleted successfully"}, 200 #successful deletion of review
