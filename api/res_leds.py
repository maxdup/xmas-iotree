from flask import current_app as app, request
from flask_restx import Resource, fields, marshal, marshal_with, abort, Namespace
from api.utils import RequestParser

import os
import json
import pika


leds_api = Namespace('Leds', path='/leds',
                     description="Leds resource")

rgb_render = leds_api.model('rgb', {
    'r': fields.Integer,
    'g': fields.Integer,
    'b': fields.Integer,
})

leds_render = leds_api.model('config', {
    'colors': fields.List(fields.Nested(rgb_render)),
})


@leds_api.route('/')
class leds_res(Resource):

    @leds_api.marshal_with(leds_render)
    def post(self):
        try:
            content = request.get_json()
            leds = content['colors']
            response = []
            colors = []
            for i in range(app.config['NLED']):
                c = leds[i % len(leds)]
                response.append(c)
                colors.append([int(c['r']), int(c['g']), int(c['b'])])

        except Exception as e:
            print(e)
            abort(400)


        message = json.dumps({'array': colors})

        connection = pika.BlockingConnection()
        channel = connection.channel()
        channel.queue_declare(queue='neopixel')
        channel.basic_publish(exchange='',
                              routing_key='neopixel',
                              body=message)
        connection.close()

        return {'colors': response}
