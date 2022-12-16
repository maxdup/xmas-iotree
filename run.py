from api import create_app, socketio
iotApp = create_app('config')

if __name__ == '__main__':
    socketio.run(iotApp, debug=True, port=5000)
    iotApp.run(host='0.0.0.0', port=8001)
