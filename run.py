from api import create_app  # , socketio

iotApp = create_app('config')

if __name__ == '__main__':
    #socketio.run(iotApp, debug=True, port=iotApp.config['DEV_PORT'])
    iotApp.run(host='0.0.0.0', debug=True, port=iotApp.config['DEV_PORT'])
