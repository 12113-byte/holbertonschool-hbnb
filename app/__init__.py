from flask import Flask, Blueprint #  Blueprint used for api isolation
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as review_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.auth import api as auth_ns
from flask_jwt_extended import JWTManager
jwt = JWTManager()

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

def create_app():
    app = Flask(__name__)
    # Create global instances                                                                                                                      
    db = SQLAlchemy()
    bcrypt = Bcrypt()
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')


    
    # Initialize extensions                                                                                                                        
    db.init_app(app)
    bcrypt.init_app(app)

    
    
    # Placeholder for API namespaces (endpoints will be added later)
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(review_ns, path='/api/v1/review')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    # Additional namespaces for places, reviews, and amenities will be added later

    
    
def create_app(config_class="config.DevelopmentConfig"): 
    #  accepts a config class as parameter, default is DevelopementConfig
    #  makes function flexible to pass different config later for testing or production
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY']='super-secret-key'
    jwt.init_app(app)
    #  app.config is a dictionary that Flask uses to store settings (needed for jwt tokens)
    #  from_object() scans the config class for UPPERCASE attributes (signals Flask "this is a setting") 
    #  and copies them into app.config, making them accessible anywhere in app
    app.config.from_object(config_class)

    # Blueprint created to group all api routes under /api/v1 prefix
    #  keeps api isolated from rest of app and prevents flask-restx from hijacking '/' route
    api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

    #  initialising flask-restx api on blueprint (not directly on app)
    #  version, title, description appear in auto-generated swagger ui
    #  doc='/doc' means swagger ui is available at /api/v1/doc
    api = Api(api_bp, version='1.0', title='HBnB API', description='HBnB Application API', doc='/doc')

    # registration of each namespace with the api
    # dealt with prefix above
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(places_ns, path='/places')
    api.add_namespace(review_ns, path='/review')
    api.add_namespace(amenities_ns, path='/amenities')

    #  registration of blueprint onto main flask app
    #  activates all /api/v1/* routes
    app.register_blueprint(api_bp)

    #  defining homepage route directly on app (not blueprint)
    #  due to flask-restx being mounted on api_bp and not on app, no conflicts
    @app.route('/')
    def homepage():
        return 'Welcome to HBnB!'

    #  returns fully configured app
    return app





    
