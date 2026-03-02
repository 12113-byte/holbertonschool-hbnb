from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
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

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        # Logic to update an amenity by ID
        data = api.payload #  get JSON from client

        try: #  try to update via BLL
            updated_amenity = facade.update_amenity(amenity_id, data)

            if updated_amenity is None:
                return {"error": "Amenity not found"}, 404
            
            return {"id": updated_amenity.id, "name": updated_amenity.name}, 200
        
        except Exception as e:
            return {"error": str(e)}, 400 # handles invalid input
