from flask import Blueprint
from flask_restx import Api

from api.res_switch import switch_api


bp_httpapi = Blueprint('iot_webapi', __name__)


httpapi = Api(bp_httpapi,
              title="IOT API",
              version='1.0',
              description='The IOT web api',
              prefix='/api',
              doc='/doc/')

httpapi.add_namespace(switch_api)
