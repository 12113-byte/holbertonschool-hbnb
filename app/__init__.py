from flask import Flask, Blueprint
from flask_restx import Api
from app.databaseimport import db, bcrypt, jwt

from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as review_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.auth import api as auth_ns


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
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

    #  registration of blueprint onto main flask app
    #  activates all /api/v1/* routes
    app.register_blueprint(api_bp)

    # Binding extensions to this app instance
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    with app.app_context():
        db.create_all()

    # registration of each namespace with the api
    # dealt with prefix above
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(auth_ns, path='/api/v1/auth')


    #  defining homepage route directly on app (not blueprint)
    #  due to flask-restx being mounted on api_bp and not on app, no conflicts
    @app.route('/')
    def homepage():
        return 'Welcome to HBnB!'

    #  returns fully configured app
    return app
