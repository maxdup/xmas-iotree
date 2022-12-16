from flask_socketio import join_room, leave_room, emit

from . import socketio


@socketio.on('join', namespace='/socket_room')
def join(message):
    """Sent by clients when they enter a room."""

    room_id = message['room_id']
    join_room(room_id)

    emit('update', {'welcome_message': 'Welcome!'}, room=room_id)


@socketio.on('leave', namespace='/socket_room')
def leave(message):
    """Sent by clients when they leave a room."""

    room_id = message['room_id']
    join_room(room_id)

    emit('update', {'welcome_message': 'Welcome!'}, room=room_id)
