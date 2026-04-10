"""
Reviews API endpoint
Handles CRUD operations for reviews:
- POST /reviews: Create a new review
- GET /reviews: Retrieve all reviews
- GET /reviews/ <review_id>: Retrieve a review by ID
- PUT /reviews/ <review_id> :Update a review (only text and rating)
- DELETE /reviews/ <review_id>: Delete a review
"""

from flask_restx import Namespace, Resource, fields
# jwt_required: blocks endpoint if no valid token is provided
# get_jwt_identity: retrieves user ID stored inside JWT token
# get_jwt: retrieves everything in token, including is_admin
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    # user_id removed - now comes from JWT token, not request
    'place_id': fields.String(required=True, description='ID of the place')
})

# Input model for updating a review (only text and rating allowed)
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required() # only authenticated user can create reviews
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new reviews"""
        # get who is making the request from their token
        current_user_id = get_jwt_identity()
        data = api.payload

        #get place being reviewd to check ownership
        place = facade.get_place(data.get('place_id'))
        if not place:
            return {"error": "Place not found"}, 404
        
        #users cannot review their own place
        if place.user_id == current_user_id:
            return {"error": "You cannot review your own place"}, 400
        
        # check if user already reviewed this place
        existing_reviews = facade.get_reviews_by_place(data['place_id'])
        for review in existing_reviews:
            if review.user_id == current_user_id:
                return {"error": "You have already reviewed this place"}, 400
            
        # set user_id from token
        data['user_id'] = current_user_id

        try:
            new_review = facade.create_review(data) #create review using facade method including validation
            print("review made")
            print(new_review)
            return {"id": new_review.id, "rating": new_review.rating, "place_id": new_review.place_id, "user_id": new_review.user_id}, 201
        except Exception as e:
            print("review err")
            return {"error": str(e)}, 400 # handles invalid input

    # GET is public, anyone can see all reviews
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{
            "id": r.id,
            "text": r.text,
            "rating": r.rating,
            "user_id": r.user_id,
            "place_id": r.place_id
        } for r in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    # GET is public, anyone can read a review
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
            "user_id": review.user_id,
            "place_id": review.place_id
        }, 200 #successful retrieval of review details

    @jwt_required() # only authenticated users can update reviews
    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorised action')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        # get ID of whoever is making request from token
        current_user = get_jwt()
        # checking if user is admin
        is_admin = current_user.get('is_admin', False)
        # extracting id
        user_id = current_user.get('id')

        # fetch review first to check ownership
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        # can only be updated by user who created it
        # bypass for admin
        if not is_admin and review.user_id != user_id:
            return {"error": "Unauthorised action"}, 403

        data = api.payload
        allowed_fields = {'text', 'rating'} #change the text and the rating based on the review id
        data = {k: v for k, v in data.items() if k in allowed_fields} # Filter input to only allowed fields
        # Attempt to update the review using the facade method
        review = facade.update_review(review_id, data)

        #return 404 if review not found
        if not review:
            return {"error": "Review not found"}, 404
        return {"message": "Review updated successfully"}, 200 #successful update of review

    @jwt_required() # only authenticated users can delete reviews
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorised action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        # get ID of whoever is making the request from token
        current_user = get_jwt()
        # checking if user is admin
        is_admin = current_user.get('is_admin', False)
        # extracting id
        user_id = current_user.get('id')

        # fetch review to check ownership
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        # only user who created review can delete it
        # bypass for admin
        if not is_admin and review.user_id != user_id:
            return {"error": "Unauthorised action"}, 403

        try:
            facade.delete_review(review_id) # Attempt to delete the review using the facade method
        except Exception as e:
            return {"error": str(e)}, 400 # handles invalid input

        return {"message": "Review deleted successfully"}, 200 #successful deletion of review

