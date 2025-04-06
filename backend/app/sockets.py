from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import JWTExtendedException  # General JWT error
from flask_socketio import emit, join_room, leave_room
from app.models import Users, Messages, Room_Users, MessageType, db

def register_socket_handlers(socketio):
    @socketio.on('connect')
    @jwt_required()
    def handle_connect():
        """
        Handle the initial connection of the user to the SocketIO server.

        Returns:
            dict: A JSON-serializable dictionary with the user's ID and status.
        """

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
        """
        Handle the 'join_room' event sent by the client. This event should contain
        an array of room IDs that the user wants to join.

        Parameters:
            data (dict): A JSON-serializable dictionary containing the room IDs to
                join. The dictionary should have a single key called 'rooms' which
                has an array of integers as its value.

        Returns:
            dict: A JSON-serializable dictionary with the status of the join
                operation. The dictionary will have a 'status' key which can be one
                of the following:

                    * 'ok': The user was successfully joined to the room(s).
                    * 'server error': An internal server error occurred while
                        attempting to join the room(s).
                    * 'authorisation error': The user is not authorized to join the
                        room(s).
        """
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
        """
        Handle the 'send_message' event from the client.

        Parameters:
            data (dict): A JSON-serializable dictionary containing the message
                data. The dictionary should have the following keys:

                    * 'room': The ID of the room to which the message should be
                        sent.
                    * 'message': The content of the message.

        Returns:
            dict: A JSON-serializable dictionary with the status of the message
                send operation. The dictionary will have a 'status' key which can
                be one of the following:

                    * 'ok': The message was successfully sent.
                    * 'server error': An internal server error occurred while
                        attempting to send the message.
                    * 'authorisation error': The user is not authorized to send
                        messages to the room.
        """
        try:
            user_id = get_jwt_identity()
            room_id = data['room']  # Zmiana z 'room_id' na 'room'
            message_content = data['message']
            message_type = data.get('message_type', MessageType.TEXT) # Only TEXT for now

            print(f"User {user_id} sending message to room {room_id}: {message_content}")
            
            # Sprawdź uprawnienia
            if not Room_Users.query.filter_by(user_id=user_id, room_id=room_id).first():
                print(f"User {user_id} is not authorized to send to room {room_id}")
                emit('message_error', {'message': 'Not authorized to send to this room'})
                return
            
            print(f"User {user_id} is authorized to send to room {room_id}")
            # Utwórz i zapisz wiadomość
            new_message = Messages(
                user_id=user_id,
                room_id=room_id,
                content=message_content,
                message_type=message_type  # Użyj typu z requestu
            )
            db.session.add(new_message)
            db.session.commit()
            print(f"Message saved with ID: {new_message.id}")
            
            # Pobierz dane użytkownika
            user = Users.query.filter_by(id=user_id).first()
            
            # Przygotuj odpowiedź zgodną z dokumentacją
            print(f"Sending response: {user.name}, {user.surname}, {message_content}, {new_message.timestamp}")
            response = {
                'name': user.name,
                'surname': user.surname,  # Dodane
                'message': message_content,
                'date': new_message.timestamp.isoformat()  # Nazwa pola 'date' zamiast 'timestamp'
            }
            
            # Wyślij do wszystkich w pokoju
            print(f"Sending response to room {room_id}: {response}")
            emit('new_message', response, room=room_id)
            
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            emit('message_error', {'message': 'Failed to send message'})