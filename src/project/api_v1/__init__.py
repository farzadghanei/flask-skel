'''
project.api_v1
--------------
API version 1 blueprint
'''

from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

from . import authentication
