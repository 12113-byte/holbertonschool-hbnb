from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as review_ns
from app.api.v1.amenities import api as amenities_ns

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

    
    
    return app





    
