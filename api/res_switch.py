from flask_restx import Resource, fields, marshal, marshal_with, abort, Namespace
from api.utils import RequestParser

#import RPi.GPIO as GPIO

switch_api = Namespace('Switch', path='/switch',
                       description="Switch resource")

switch_render = switch_api.model('switch_status', {
    'status': fields.String,
})

args = {'status': {'required': True}}
request_parser = RequestParser(arguments=args)

SIGNAL = 18


def gpio_open():
    GPIO.output(SIGNAL, GPIO.HIGH)


def gpio_close():
    GPIO.output(SIGNAL, GPIO.LOW)


class switch_res(Resource):

    @switch_api.marshal_with(switch_render)
    def get(self):
        return {'status': 'online'}

    @switch_api.expect(request_parser)
    @switch_api.marshal_with(switch_render)
    def post(self):
        content = request_parser.parse_args()
        if content['status'] == 'open':
            gpio_open()
            return {status: 'open'}

        elif content['status'] == 'close':
            gpio_close()
            return {'status': 'close'}

        else:
            return {'status': 'error'}
