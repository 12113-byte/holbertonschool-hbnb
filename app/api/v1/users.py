from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new User"""
        user_data = api.payload

        try:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return({'error': 'Email already registered'}), 400

            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201

        except Exception as e:
            api.abort(400, str(e))
    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'Success')
    @api.response(404, 'User not found')

    def get(self, user_id):
        """Get a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200
    
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
<<<<<<< HEAD
    @jwt_required()
=======
>>>>>>> db4e54a5eb36a9cea3e77632a08b5ae56eb459f8
    def put(self, user_id):
        """Update a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        try:
            facade.update_user(user_id, api.payload)
            return "User Updated", 200

        except Exception as e:
            api.abort(400, str(e))
