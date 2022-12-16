from flask import request
from flask_restx import Resource, fields, marshal, marshal_with, abort, Namespace
from api.utils import RequestParser

import os
import json

config_api = Namespace('Config', path='/config',
                       description="Config resource")
NLED = 50

pos_render = config_api.model('position', {
    'x': fields.Float,
    'y': fields.Float,
    'z': fields.Float,
})
bounds_render = config_api.model('bounds', {
    'min': fields.Nested(pos_render),
    'max': fields.Nested(pos_render)
})
config_render = config_api.model('config', {
    'positions': fields.List(fields.Nested(pos_render)),
    'bounding_box': fields.Nested(bounds_render),
    'led_count': fields.Integer(),
})


def make_response(conf):
    return {**conf, **{
        'led_count': NLED,
        'bounding_box': {
            'min': {'x': -1, 'y': -1, 'z': -1},
            'max': {'x': 1, 'y': 1, 'z': 1}}
    }}


@config_api.route('/')
class config_res(Resource):

    @config_api.marshal_with(config_render)
    def get(self):
        config = {'positions': [[], [], []]}
        try:
            with open('data/config.json', 'r') as f:
                config = json.load(f)
        except Exception as e:
            abort(404)

        return make_response(config)

    @config_api.marshal_with(config_render)
    def post(self):
        try:
            content = request.get_json()
            config = {'positions': []}
            for i in range(NLED):
                pos = content['positions'][i % len(content)]
                config['positions'].append({'x': pos['x'],
                                            'y': pos['y'],
                                            'z': pos['z']})
        except Exception as e:
            return abort(400)

        os.makedirs('data', exist_ok=True)
        with open("data/config.json", "w+") as f:
            json.dump(config, f)

        return make_response(config)
