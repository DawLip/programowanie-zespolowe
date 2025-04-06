from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import JWTExtendedException  # General JWT error
from flask_socketio import emit, join_room, leave_room
from app.models import Users, Messages, Room_Users, MessageType, db

def register_socket_handlers(socketio):
    @socketio.on('connect')
    @jwt_required()
    def handle_connect():
        try:
            print("\n=== SocketIO connected ===")
            user_id = get_jwt_identity()
            print(f"User {user_id} connected")
            emit('connection_established', {'user_id': user_id})
            return {'status': 'ok'}
        # authorization error
        except JWTExtendedException as e:
            print(f"Authorisation error: {str(e)}")
            return {'status': 'authorisation error'}
        # server error
        except Exception as e:
            print(f"Error connecting: {str(e)}")
            return {'status': 'server error'}

    @socketio.on('join_room')
    @jwt_required()
    def handle_join_room(data):
        print("\n=== SocketIO join_room called ===")
        user_id = get_jwt_identity()
        room_ids = data.get('rooms', [])

        if not isinstance(room_ids, list):
            emit('join_room_response', {
                'status': 'server error',
                'message': 'Invalid rooms format - expected array'
            })
            return

        for room_id in room_ids:
            try:
                print(f"User {user_id} attempting to join room {room_id}")
                
                if Room_Users.query.filter_by(user_id=user_id, room_id=room_id).first():
                    join_room(room_id)
                    emit('join_room_response', {
                        'status': 'ok',
                        f'message': 'Successfully joined room {room_id}'  # Generic success message
                    })
                else:
                    emit('join_room_response', {
                        'status': 'authorisation error',
                        f'message': 'Not authorized to join room {room_id}'
                    })

            except Exception as e:
                print(f"Error joining room {room_id}: {str(e)}")
                emit('join_room_response', {
                    'status': 'server error',
                    'message': 'Failed to join rooms'
                })

    @socketio.on('leave_room')
    @jwt_required()
    def handle_leave_room(data):
        user_id = get_jwt_identity()
        room_id = data['room_id']
        print(f"User {user_id} wants to leave room {room_id}")
        leave_room(room_id)

    @socketio.on('send_message')
    @jwt_required()
    def handle_send_message(data):
        try:
            user_id = get_jwt_identity()
            room_id = data['room_id']
            message_content = data['message']

            print(f"User {user_id} wants to send message to room {room_id}: {message_content}")
            
            if not Room_Users.query.filter_by(user_id=user_id, room_id=room_id).first():
                emit('message_error', {'message': 'Not authorized to send to this room'})
                return
            
            new_message = Messages(
                user_id=user_id,
                room_id=room_id,
                content=message_content,
                message_type=MessageType.TEXT
            )
            db.session.add(new_message)
            db.session.commit()
            
            emit('new_message', {
                'user_id': user_id,
                'room_id': room_id,
                'message': message_content,
                'timestamp': new_message.timestamp.isoformat(),
                'name': Users.query.filter_by(id=user_id).first().name
            }, room=room_id)
            
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            emit('message_error', {'message': 'Failed to send message'})