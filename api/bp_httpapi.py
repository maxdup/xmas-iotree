from flask import Blueprint
from flask_restx import Api


from api.res_config import config_api
from api.res_leds import leds_api


bp_httpapi = Blueprint('iot_webapi', __name__)


httpapi = Api(bp_httpapi,
              title="IOT API",
              version='1.0',
              description='The IOT web api',
              prefix='/api',
              doc='/doc/')

httpapi.add_namespace(config_api)
httpapi.add_namespace(leds_api)
