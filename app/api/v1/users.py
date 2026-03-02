from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'age': fields.Integer(required=True),
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model)
    @api.response(201, 'User created')
    @api.response(400, 'Bad request')
    def post(self):
        user_data = api.payload
        try:
            user = facade.create_user(api.payload)
            return user.to.dict()
        except Exception as e:
            api.abort(400, str(e))

    @api.response(200, 'Success')
    def get(self):
        """Get all users"""
        return [user.to.dict() for user in facade.get_all_users()]
    
@api.route('/<int:user_id>')
class UserResource(Resource):

    @api.response(200, 'Success')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get a user by ID"""
        user = facade.get_user_by_id(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user.to.dict()
    
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update a user by ID"""
        try:
            user = facade.update_user(user_id, api.payload)
            if not user:
                api.abort(404, 'User not found')
            return user.to.dict(), 200
        except Exception as e:
            api.abort(400, str(e))
