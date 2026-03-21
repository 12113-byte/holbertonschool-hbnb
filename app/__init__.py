from flask import Flask, Blueprint
from flask_restx import Api
from app.databaseimport import db, bcrypt

from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as review_ns
from app.api.v1.amenities import api as amenities_ns

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    bcrypt.init_app(app)
    db.init_app(app)

    # Placeholder for API namespaces (endpoints will be added later)
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(review_ns, path='/api/v1/review')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    app.register_blueprint(api_bp)

    @app.route('/')
    def homepage():
        return 'Welcome to HBnB!'

    return app
