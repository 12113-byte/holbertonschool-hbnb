from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.review import api as review_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.auth import api as auth_ns
from flask_jwt_extended import JWTManager
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY']='super-secret-key'
    jwt.init_app(app)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Placeholder for API namespaces (endpoints will be added later)
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(review_ns, path='/api/v1/review')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    # Additional namespaces for places, reviews, and amenities will be added later
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
