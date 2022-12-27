from flask import current_app as app, request, make_response
from flask_restx import Resource, fields, marshal, marshal_with, abort, Namespace
from api.utils import RequestParser

import os
import json
import pika

script_api = Namespace('Script', path='/script',
                       description="script resource")


def getScriptDir():
    scriptDir = os.path.join(os.path.dirname(__file__), '..')
    scriptDir = os.path.join(scriptDir, app.config['SCRIPTS_FOLDER'])
    return scriptDir


def list_scripts():
    sdir = getScriptDir()
    return [f for f in os.listdir(sdir) if f.endswith(".py") and not f.startswith('_')]


def get_filepath(filename=None):
    filename = os.path.basename(filename)
    if not filename.endswith('.py'):
        filename += '.py'
    return os.path.join(getScriptDir(), filename)


def get_file(filename=None):
    if not filename:
        raise Exception("no filename")
    filepath = get_filepath(filename)

    if not os.path.isfile(filepath):
        raise Exception("file missing")

    with open(filepath, 'r') as f:
        content = f.read()

    return content


def write_file(filename=None, content=None):
    if not filename:
        raise Exception("no filename")
    filepath = get_filepath(filename)

    with open(filepath, 'w', encoding="utf-8") as f:
        f.write(content)


def run_file(filename=None):
    if not filename:
        raise Exception("no filename")
    filepath = get_filepath(filename)

    message = json.dumps({'run_script': os.path.abspath(filepath)})

    connection = pika.BlockingConnection()
    channel = connection.channel()
    channel.queue_declare(queue='neopixel')
    channel.basic_publish(exchange='',
                          routing_key='neopixel',
                          body=message)
    connection.close()


def stop_file(filename=None):
    if not filename:
        raise Exception("no filename")
    filepath = get_filepath(filename)

    message = json.dumps({'kill_script': os.path.abspath(filepath)})

    connection = pika.BlockingConnection()
    channel = connection.channel()
    channel.queue_declare(queue='neopixel')
    channel.basic_publish(exchange='',
                          routing_key='neopixel',
                          body=message)
    connection.close()


@script_api.route('/')
@script_api.route('/<string:_filename>')
class scripts_res(Resource):

    def get(self, _filename=None):
        if _filename:
            try:
                content = get_file(_filename)
            except Exception as e:
                if e.args == 'file missing':
                    abort(404)
                else:
                    abort(400)

            response = make_response(content, 200)
            response.mimetype = "text/plain;charset=utf-8"
            return response
        else:
            scripts = list_scripts()
            content = json.dumps({'scripts': scripts})
            response = make_response(content, 200)
            response.mimetype = "application/json"
            return response

    def post(self, _filename=None):
        if not _filename:
            abort(404)
        try:
            content = request.get_data(as_text=True)
            write_file(_filename, content)

        except Exception as e:
            print(e)
            abort(400)

        response = make_response(content, 200)
        response.mimetype = "text/plain;charset=utf-8"
        return response

    def put(self, _filename=None):
        if not _filename:
            abort(404)
        try:
            run_file(_filename)
        except Exception as e:
            if e.args == 'file missing':
                abort(404)
            else:
                print(e)
                abort(400)
        return make_response('', 200)

    def delete(self, _filename=None):
        if not _filename:
            abort(404)
        try:
            run_file(_filename)
        except Exception as e:
            if e.args == 'file missing':
                abort(404)
            else:
                print(e)
                abort(400)
        return make_response('', 200)
