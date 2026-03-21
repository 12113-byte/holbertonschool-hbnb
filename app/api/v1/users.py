from flask_restx import Namespace, Resource, fields
# jwt_required: blocks endpoint if no valid token is provided
# get_jwt: retrieves everything in token, including is_admin
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# separate update model - email and password excluded intentionally
# regular users are not allowed to change these via this endpoint
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
})

@api.route('/')
class UserList(Resource):
    # POST /users/ only admin can create users
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new User"""
        # get whoever is making request from token
        current_user = get_jwt()
        # access only for admin
        if not current_user.get('is_admin'):
            return {"error": "Admin privileges required"}, 403

        user_data = api.payload

        try:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return({'error': 'Email already registered'}), 400

            print("Creating new user")
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201

        except Exception as e:
            api.abort(400, str(e))
    
@api.route('/<user_id>')
class UserResource(Resource):
    # GET is public, anyone can loop up a user profile
    @api.response(200, 'Success')
    @api.response(404, 'User not found')

    def get(self, user_id):
        """Get a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @jwt_required() # only authenticated users can update their profile
    @api.expect(user_model) # no validation to get admin requests through
    @api.response(200, 'User updated')
    @api.response(403, 'Unauthorised action')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        """Update a user by ID"""
        # get who is making request from token
        current_user = get_jwt()
        # checking if user is admin
        is_admin = current_user.get('is_admin', False)
        # extracting token id
        token_user_id = current_user.get('id')

        # retrieving data from request
        data = api.payload

        # users can only update their own profile
        # if user_id in the URL does not match token: block them!
        # bypass for admin
        if is_admin:
            email = data.get('email')
            if email:
                existing_user = facade.get_user_by_email(email)
                if existing_user and existing_user.id != user_id:
                    return {"error": "Email already in use"}, 400
            facade.update_user(user_id, data)
            return "User Updated", 200
        else:
            # regular user can only update their own profile
            if user_id != token_user_id:
                return {"error": "Unauthorised action"}, 403

            # extra safety check, in case they somehow pass email or password.
            # rejecting it here before it reaches database
            if 'email' in data or 'password' in data:
                return {"error": "You cannot modify email or password"}, 400

            user = facade.get_user(user_id)
            if not user:
                return {"error": "User not found"}, 404

            try:
                facade.update_user(user_id, data)
                return "User Updated", 200

            except Exception as e:
                api.abort(400, str(e))
