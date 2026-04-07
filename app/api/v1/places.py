"""
Places API endpoint
Handles CRUD operations for places:
- POST /places: Create a new place
- GET /places: Retrieve all places
- GET /places/ <place_id>: Retrieve a place by ID
- PUT /places/ <place_id>: Update a place
- DELETE /places/ <place_id>: Delete a place
"""

from flask_restx import Namespace, Resource, fields
# jwt_required: blocks endpoint if no valid token is provided
# get_jwt_identity: retrieves user ID stored inside JWT token
# get_jwt: retrieves everything in token, including is_admin
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

#Created namespace
api = Namespace('places', description='Place operations')

#Amenity output format
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})
user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

#Review format
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

#Place Format
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'image': fields.String(required=False, description='Image of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    # owner_id removed - now comes from JWT token, not request
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

#Places
@api.route('/')
class PlaceList(Resource):
    @jwt_required() # blocks request if no valid JWT token is provided in the header
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place created')
    @api.response(400, 'Invalid data')
    @api.response(404, 'User not found')
    def post(self):
        """Creates new Place"""
        # get_jwt_identity() reads the user ID which was stored in token at login
        # safer than trusting owner_id from request body
        current_user_id = get_jwt_identity()

        data = api.payload

        # setting owner_id from token, not what client sent
        # prevents users from creating places on behalf of other users
        data['owner_id'] = current_user_id

        try:
            place = facade.create_place(data)
            # Return minimal response
            return {
                "id": place.id,
                "title": place.title,
                "image": place.image,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner_id": place.user_id
            }, 201

        except Exception as e:
            return {"error": str(e)}, 400

    # ---------------------------------
    # GET is public, no jwt_required needed
    @api.response(200, 'Places retrieved')
    def get(self):
        """Get all Places"""
        places = facade.get_all_places()

        return [{
            "id": p.id,
            "title": p.title,
            "image": p.image,
            "description": p.description,
            "price": p.price,
            "latitude": p.latitude,
            "longitude": p.longitude
        } for p in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    # GET is public, anyone can view a place's details
    @api.response(200, 'Place found')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get a specific Place"""
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        return {
            "place": {
                "id": place_id,
                "title": place.title,
                "image": place.image,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude
            },
            # Owner relationship
            "owner": {
                "id": place.user.id,
                "first_name": place.user.first_name,
                "last_name": place.user.last_name,
                "email": place.user.email
            },
            "reviews" : [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user_id
            } for r in place.reviews
            ],
            "amenities": [{"id": a.id, "name": a.name} for a in place.amenities],
            }, 200

    # ---------------------------------

    @jwt_required() # only authenticated users can update a place
    @api.expect(place_model)
    @api.response(200, 'Updated')
    @api.response(403, 'Unauthorised action')
    @api.response(404, 'Not found')
    @api.response(400, 'Error Updating Place')
    def put(self, place_id):
        """Update a Place"""
        # get ID of whoever is making this request from token
        current_user = get_jwt()
        # checking if user is admin
        is_admin = current_user.get('is_admin', False)
        # extracting id
        user_id = get_jwt_identity()

        # fetch place from database
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        # ownership check: does place belong to this user? if no: block them
        # place.owner_id is who owns the place, user_id is who's asking
        # bypass for admin
        if not is_admin and place.user_id != user_id:
            return {"error": "Unauthorised action"}, 403
        
        data = api.payload
        try:
            updated = facade.update_place(place_id, data)
            return {"message": "Place updated successfully"}, 200

        except Exception as e:
            return {"error": str(e)}, 400


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Placeholder for logic to return a list of reviews for a place
        # Verify the place exists
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        
        # Fetch all reviews linked to this place via the facade
        reviews = facade.get_reviews_by_place(place_id)

        # Return serialized list of reviews
        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user_id
            } for r in reviews
        ], 200
