from flask import current_app as app, request
from flask_restx import Resource, fields, marshal, marshal_with, abort, Namespace
from api.utils import RequestParser

import os
import json

isPI = os.uname()[4][:3] == 'arm'

try:
    import board
    import neopixel
except ImportError:
    if isPI:
        print('import error for neopixel')

if isPI:
    pixels = neopixel.NeoPixel(board.D18, app.config['NLED'], brightness=0.25,
                               pixel_order=neopixel.RGB, auto_write=False)


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


def apply_leds(color_array):
    output = []
    for i in range(app.config['NLED']):
        c = color_array[i % len(color_array)]
        output.append(c)
        if isPI:
            pixels[i] = (c['r'], c['g'], c['b'])
    if isPI:
        pixels.show()

    return output


@leds_api.route('/')
class leds_res(Resource):

    @leds_api.marshal_with(leds_render)
    def post(self):
        try:
            content = request.get_json()
            leds = content['colors']
            output = apply_leds(leds)
            response = None

        except Exception as e:
            print(e)
            abort(400)

        connection = pika.BlockingConnection()
        channel = connection.channel()
        channel.basic_publish(exchange='test', routing_key='test',
                              body=b'Test message.')
        connection.close()

        return {'colors': output}
