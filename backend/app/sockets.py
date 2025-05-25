from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import JWTExtendedException  # General JWT error
from flask_socketio import emit, join_room, leave_room
from app.models import Users, Messages, Room_Users, MessageType, db
import base64
import os
from datetime import datetime
from werkzeug.utils import secure_filename

def register_socket_handlers(socketio):
    @socketio.on('connect')
    @jwt_required()
    def handle_connect():
        """
        Obsługuje zdarzenie 'connect' wysyłane przez klienta. Wymaga autoryzacji JWT.

        Zwraca:
            dict: JSON-serializowalny słownik z informacją o statusie połączenia.
            Słownik zawiera klucz 'status', który może mieć jedną z poniższych wartości:
            
                * 'ok': Użytkownik został pomyślnie połączony.
                * 'authorisation error': Wystąpił błąd autoryzacji JWT.
                * 'server error': Wystąpił wewnętrzny błąd serwera podczas próby połączenia.
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
        Obsługuje zdarzenie 'join_room' wysyłane przez klienta. Wymaga autoryzacji JWT.

        Parameters:
            data (dict): JSON-serializowalny słownik z informacją o pokojach do których
                użytkownik chce dołączyć. Słownik powinien zawierać klucz 'rooms' o
                wartości będącej listą identyfikatorów pokojów (int).

        Returns:
            dict: JSON-serializowalny słownik z informacją o statusie operacji
                dołączenia do pokojów. Słownik zawiera klucze 'status' i 'message'.
                Wartość 'status' może być jedną z poniższych:

                    * 'ok': Użytkownik został pomyślnie dołączony do pokojów.
                    * 'authorisation error': Wystąpił błąd autoryzacji JWT.
                    * 'server error': Wystąpił wewnętrzny błąd serwera podczas próby
                        dołączenia do pokojów.

                Wartość 'message' to wiadomość dla użytkownika z dodatkowymi
                informacjami o błędzie.
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
                    print(f"User {user_id} joined room {room_id}")
                    join_room(room_id)
                    emit('join_room_response', {
                        'status': 'ok',
                        'message': f'Successfully joined room {room_id}'  # Generic success message
                    })
                else:
                    print(f"User {user_id} is not authorized to join room {room_id}")
                    emit('join_room_response', {
                        'status': 'authorisation error',
                        'message': f'Not authorized to join room {room_id}'
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
        """
        Obsługuje zdarzenie 'leave_room' wysyłane przez klienta. Wymaga autoryzacji JWT.

        Parameters:
            data (dict): JSON-serializowalny słownik z informacją o pokojach z
                których użytkownik chce opuścić. Słownik powinien zawierać klucz
                'room_id' o wartości będącej identyfikatorem pokoju (int).

        Returns:
            None
        """
        user_id = get_jwt_identity()
        room_id = data['room_id']
        print(f"User {user_id} wants to leave room {room_id}")
        leave_room(room_id)

    @socketio.on('refresh')
    @jwt_required()
    def handle_refresh(data):
        """
        Obsługuje zdarzenie 'refresh' wysyłane przez klienta. Wymaga autoryzacji JWT.

        Parameters:
            data (dict): JSON-serializowalny słownik z informacją o odświeżeniu.
                Słownik powinien zawierać klucz 'message' o wartości będącej
                wiadomością do wyświetlenia w konsoli klienta.

        Returns:
            None
        """
        socketio.emit('refresh', {'message': 'refresh'})
    
    @socketio.on('send_message')
    @jwt_required()
    def handle_send_message(data):
        """
        Obsługuje zdarzenie 'send_message' wysyłane przez klienta. Wymaga autoryzacji JWT.

        Parameters:
            data (dict): JSON-serializowalny słownik zawierający informacje o wiadomości.
                Słownik powinien zawierać następujące klucze:
                    - 'room': identyfikator pokoju, do którego wiadomość ma zostać wysłana.
                    - 'message': treść wiadomości.
                    - 'message_type' (opcjonalnie): typ wiadomości, domyślnie MessageType.TEXT.

        Działanie:
            1. Weryfikuje, czy użytkownik ma uprawnienia do wysyłania wiadomości do
            wskazanego pokoju.
            2. Zapisuje wiadomość w bazie danych przy użyciu modelu Messages.
            3. Emituje zdarzenie 'new_message' z informacjami o wiadomości do
            wszystkich użytkowników w pokoju.

        Obsługa błędów:
            - Emituje 'message_error' z odpowiednim komunikatem w przypadku braku
            uprawnień lub błędów serwerowych podczas wysyłania wiadomości.
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
                'message_id': new_message.id,
                'group_id': room_id,
                'user_id': user.id,
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
            
# # Konfiguracja
# UPLOAD_FOLDER = 'static/uploads'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# @socketio.on('send_image')
# @jwt_required()
# def handle_send_image(data):
#     """
#     Handle image upload and sending through websocket.
    
#     Parameters:
#         data (dict): Contains:
#             - 'room': room ID
#             - 'image_data': base64 encoded image
#             - 'filename': original filename
#             - 'file_size': size in bytes
#     """
#     try:
#         user_id = get_jwt_identity()
#         room_id = data['room']
        
#         # Sprawdź uprawnienia
#         if not Room_Users.query.filter_by(user_id=user_id, room_id=room_id).first():
#             emit('image_error', {'message': 'Not authorized to send to this room'})
#             return

#         # Walidacja danych
#         if not all(key in data for key in ['image_data', 'filename', 'file_size']):
#             emit('image_error', {'message': 'Missing required fields'})
#             return

#         if data['file_size'] > MAX_FILE_SIZE:
#             emit('image_error', {'message': f'File too large (max {MAX_FILE_SIZE/1024/1024}MB)'})
#             return

#         # Przygotuj folder na upload
#         os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#         # Generuj unikalną nazwę pliku
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         filename = secure_filename(f"{user_id}_{timestamp}_{data['filename']}")
#         filepath = os.path.join(UPLOAD_FOLDER, filename)

#         # Zapisz obraz (base64 -> plik)
#         image_data = data['image_data'].split(",")[1]  # Usuń nagłówek (np. "data:image/png;base64,")
#         with open(filepath, "wb") as f:
#             f.write(base64.b64decode(image_data))

#         # Zapisz wiadomość
#         new_message = Messages(
#             user_id=user_id,
#             room_id=room_id,
#             content=filename,  # Przechowujemy nazwę pliku
#             message_type=MessageType.IMAGE,
#             image_path=filepath
#         )
#         db.session.add(new_message)
#         db.session.commit()

#         # Przygotuj odpowiedź
#         user = Users.query.get(user_id)
#         response = {
#             'message_id': new_message.id,
#             'user_id': user.id,
#             'name': user.name,
#             'surname': user.surname,
#             'image_url': f"/{filepath}",  # URL względny
#             'thumbnail_url': f"/{generate_thumbnail(filepath)}",  # Opcjonalnie
#             'date': new_message.timestamp.isoformat(),
#             'original_filename': data['filename']
#         }

#         emit('new_image', response, room=room_id)

#     except Exception as e:
#         print(f"Error sending image: {str(e)}")
#         emit('image_error', {'message': 'Failed to send image'})