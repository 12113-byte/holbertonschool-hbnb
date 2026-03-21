from flask import Blueprint
from flask_restx import Api

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, title='HBNB API', version='1.0')

