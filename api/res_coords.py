from flask import current_app as app, request, make_response
from flask_restx import Resource, fields, marshal, marshal_with, abort, Namespace
from api.utils import RequestParser

import os
import json

coords_api = Namespace('Coordinates', path='/coords',
                       description="Coordinates resource")


def respond(conf):
    content = json.dumps(conf)
    response = make_response(content, 200)
    return response


COORD_FILENAME = 'data/coordinates.json'


@coords_api.route('/')
class coords_res(Resource):

    def get(self):
        coord_system = {'coords': []}
        try:
            with open(COORD_FILENAME, 'r') as f:
                coord_system = json.load(f)
        except Exception as e:
            abort(404)

        return respond(coord_system)

    def post(self):
        try:
            content = request.get_json()
            coord_system = {}
            coord_system['coords'] = content['coords']
            coord_system['nled'] = len(coord_system['coords'])
            coord_system['bounding_box'] = {
                'min': [-1, -1, -1],
                'max': [1, 1, 1]}

        except Exception as e:
            print(e)
            return abort(400)

        os.makedirs('data', exist_ok=True)
        with open(COORD_FILENAME, "w+") as f:
            json.dump(coord_system, f)

        return respond(coord_system)
