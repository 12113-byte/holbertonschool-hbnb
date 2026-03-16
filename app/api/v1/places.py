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
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

#Places
@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place created')
    @api.response(400, 'Invalid data')
    @api.response(404, 'User not found')
    @jwt_required()
    def post(self):
        """Creates new Place"""
        data = api.payload
        try:
            place = facade.create_place(data)
            # Return minimal response
            return {
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner_id": place.owner.id
            }, 201

        except Exception as e:
            return {"error": str(e)}, 400

    # ---------------------------------

    @api.response(200, 'Places retrieved')
    def get(self):
        """Get all Places"""
        places = facade.get_all_places()

        return [{
            "id": p.id,
            "title": p.title,
            "latitude": p.latitude,
            "longitude": p.longitude
        } for p in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
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
                "description": place.description,
                "latitude": place.latitude,
                "longitude": place.longitude
            },
            # Owner relationship
            "owner": {
                "id": place.owner.id,
                "first_name": place.owner.first_name,
                "last_name": place.owner.last_name,
                "email": place.owner.email
            },
            "reviews" : [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user_id
            } for r in place.reviews
            ],
            "amenities": [a.id for a in place.amenities],
            }, 200

    # ---------------------------------

    @api.expect(place_model)
    @api.response(200, 'Updated')
    @api.response(404, 'Not found')
    @api.response(400, 'Error Updating Place')
    @jwt_required()
    def put(self, place_id):
        #updates allowed fields for the specified place
        data = api.payload
        try:
            place = facade.update_place(place_id, data)
            if not place:
                return {"error": "Place not found"}, 404

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
                "user_id": r.user.id
            } for r in reviews
        ], 200
