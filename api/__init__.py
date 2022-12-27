import os
from flask import Flask, Config, url_for
#from flask_socketio import SocketIO
from flask_cors import CORS

#socketio = SocketIO(cors_allowed_origins='*')  # NOQA: E402

from api.bp_httpapi import bp_httpapi
#from api.bp_sockets import *
from api.bp_webapp import bp_webapp


def create_app(config):
    template_dir = os.path.join(os.path.dirname(__file__), '..')
    template_dir = os.path.join(template_dir, 'webapp/build')
    app = Flask('iotree',
                static_folder=template_dir,
                template_folder=template_dir)
    CORS(app)

    app.config.from_object(config)
    app.url_map.strict_slashes = True

    app.register_blueprint(bp_httpapi)
    app.register_blueprint(bp_webapp)

    # socketio.init_app(app)

    return app
