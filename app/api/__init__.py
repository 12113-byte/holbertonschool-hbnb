from flask import Blueprint
from flask_restx import Api
from app.api.v1.views import api as users_ns

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, title='HBNB API', version='1.0')

api.add_namespace(users_ns, path='/users')
