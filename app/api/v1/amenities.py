"""
Amenities API endpoint
Handles CRUD operations for amenities:
- POST /amenities: Create a new amenity
- GET /amenities: Retrieve all amenities
- GET /amenities/ <amenity_id>: Retrieve an amenity by ID
- PUT /amenities/ <amenity_id>: Update an amenity
- DELETE /amenities/ <amenity_id>: Delete an amenity
"""

from flask_restx import Namespace, Resource, fields
# jwt_required: blocks endpoint if no valid token is provided
# get_jwt: retrieves everything in token, including is_admin
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @jwt_required() # only admin has access
    @api.expect(amenity_model)
    @api.response(403, 'Unauthorised action')
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        # get whoever is making request from token
        current_user = get_jwt()
        # access only for admin
        if not current_user.get('is_admin'):
            return {"error": "Admin privileges required"}, 403

        data = api.payload
        try:
            new_amenity = facade.create_amenity(data) #  create new amenity
            return {"id": new_amenity.id, "name": new_amenity.name}, 201
        except Exception as e:
            return {"error": str(e)}, 400

    """
        Get All Amenities
    """
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        # Logic to return a list of all amenities
        all_amenities = facade.get_all_amenities() #  call the business logic layer
        amenities_list = [] #convert each amenity object to a dictionary
        for amenity in all_amenities:
            amenities_list.append({"id": amenity.id, "name": amenity.name})
        
        return amenities_list, 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        # Logic to retrieve an amenity by ID
        amenity = facade.get_amenity(amenity_id) # call bll to fetch amenity

        if amenity is None:
            return {"error": "Amenity not found"}, 404
        
        return {"id": amenity.id, "name": amenity.name}, 200 #  return amenity as dictionary

    @jwt_required() # only admin has access
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(403, 'Unauthorised action')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        # get whoever is making request from token
        current_user = get_jwt()
        # access only for admin
        if not current_user.get('is_admin'):
            return {"error": "Admin privileges required"}, 403

        data = api.payload
        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            return {"error": "Amenity not found"}, 404

        try:
            facade.update_amenity(amenity_id, data)
            return "Amenity updated successfully", 200
        
        except Exception as e:
            return {"error": str(e)}, 400 # handles invalid input
