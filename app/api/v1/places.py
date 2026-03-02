from flask_restx import Namespace, Resource, fields
from app.services import facade

#Created namespace
api = Namespace('places', description='Place operations')

#Amenity output format
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String,
    'name': fields.String
})

#Owner output format
user_model = api.model('PlaceUser', {
    'id': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String
})

#Input model for creating/updating places
place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.String)
})

#Places
@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place created')
    @api.response(400, 'Invalid data')
    def post(self):
        #Creates new place
        try:
            data = api.payload
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
        #Get detailed place info
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "latitude": place.latitude,
            "longitude": place.longitude,

            # Owner relationship
            "owner": {
                "id": place.owner.id,
                "first_name": place.owner.first_name,
                "last_name": place.owner.last_name,
                "email": place.owner.email
            },

            # Amenities relationship
            "amenities": [
                {"id": a.id, "name": a.name}
                for a in place.amenities
            ]
        }, 200

    # ---------------------------------

    @api.expect(place_model)
    @api.response(200, 'Updated')
    @api.response(404, 'Not found')
    @api.response(400, 'Error Updating Place')
    def put(self, place_id):
        #updates the place
        data = api.payload
        try:
            place = facade.update_place(place_id, data)
            if not place:
                return {"error": "Place not found"}, 404

            return {"message": "Place updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 400
