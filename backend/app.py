from flask import Flask, jsonify, request, abort, render_template, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, Users, Messages, Room, Room_Users, Role, MessageType
from flask_socketio import SocketIO, emit, join_room, leave_room
from sqlalchemy.orm import sessionmaker
import bcrypt
from flask import request, jsonify
from sqlalchemy import or_, and_

app = Flask(__name__)
# Konfiguracja JWT
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

# Konfiguracja Socket.IO
socketio = SocketIO(app)

# Konfiguracja bazy danych SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) # Inicjalizacja bazy danych
with app.app_context():
    db.create_all()  # Tworzenie tabel w bazie danych
    # Konfiguracja sesji
    Session = sessionmaker(bind=db.engine)
    session = Session()

# Strona główna z listą użytkowników
@app.route('/')
def index():
    users = Users.query.all()
    return render_template('chat.html', users=users)

# Rejestracja nowego użytkownika
@app.route('/auth/register', methods=['POST'])
def register():
    # Pobieranie danych z formularza/JSON, choose one
    data = request.get_json()
    # data = request.form.get()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    surname = data.get('surname')

    if not email or not password:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
    
    # if email is taken
    if Users.query.filter_by(email=email).first():
        return jsonify({"status": "email is taken"}), 400
    
    # Hashowanie hasła
    # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Tworzenie nowego uzytkownika
    new_user = Users(email=email, password=password, name=name, surname=surname)
    # new_user = Users(email=email, password=hashed_password.decode('utf-8'), name=name, surname=surname)
    db.session.add(new_user)
    db.session.commit()

    # Tworzenie tokenu JWT
    access_token = create_access_token(identity=new_user.id)

    return jsonify({"status": "success", "access_token": access_token}), 200

# Logowanie
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"status": "error", "message": "Missing email or password"}), 400

    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    # Verify password - IMPORTANT: In production, use proper password hashing!
    if password == user.password:  # Changed from data.get('password')
        # Ensure identity is a string
        access_token = create_access_token(identity=str(user.id))  # Convert to string
        return jsonify({
            "status": "success",
            "access_token": access_token,
            # "user_id": user.id  # For debugging
        }), 200
    else:
        return jsonify({"status": "error", "message": "Invalid email or password"}), 401

@app.route('/users/search', methods=['GET'])
def search_users():
    search_query = request.args.get('query', '').strip()
    
    if not search_query or len(search_query) < 2:
        return jsonify({"status": "error", "message": "Query must be at least 2 characters long"}), 400

    try:
        query_parts = search_query.split()
        
        # Szukanie imie+nazwisko
        if len(query_parts) >= 2:
            users = Users.query.filter(
                and_(
                    Users.name.ilike(f'%{query_parts[0]}%'),
                    Users.surname.ilike(f'%{query_parts[1]}%')
                )
            ).limit(20).all()
        else:
            # szukanie imie lub nazwisko
            users = Users.query.filter(
                or_(
                    Users.name.ilike(f'%{query_parts[0]}%'),
                    Users.surname.ilike(f'%{query_parts[0]}%')
                )
            ).limit(20).all()

        results = [{
            "id": user.id,
            "name": user.name,
            "surname": user.surname
        } for user in users]

        return jsonify({
            "status": "success",
            "count": len(results),
            "users": results
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

################# Bonus Endpoints #################

@app.route('/api/my-rooms', methods=['GET'])
@jwt_required()
def get_my_rooms():
    print("\n=== /api/my-rooms called ===")
    # print("Request headers:", dict(request.headers))  # Verify Authorization header
    
    try:
        user_id = get_jwt_identity()
        print("Decoded user_id from JWT:", user_id)
        
        rooms = Room.query.join(Room_Users).filter(Room_Users.user_id == user_id).all()
        print("SQL query executed. Found rooms:", [r.name for r in rooms])
        
        return jsonify({
            "status": "success",
            "rooms": [{"id": r.id, "name": r.name} for r in rooms]
        })
    except Exception as e:
        print("ERROR in my-rooms:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/api/rooms/<int:room_id>/messages', methods=['GET'])
@jwt_required()
def get_room_messages(room_id):
    user_id = get_jwt_identity()
    print(f"User {user_id} wants to get messages for room {room_id}")
    
    # Verify room membership
    if not Room_Users.query.filter_by(user_id=user_id, room_id=room_id).first():
        return jsonify({'error': 'Not authorized'}), 403
    
    # Join with Users table to get the sender's name
    messages = db.session.query(
        Messages,
        Users.name
    ).join(
        Users, Messages.user_id == Users.id
    ).filter(
        Messages.room_id == room_id
    ).order_by(
        Messages.timestamp.asc()
    ).all()
    
    return jsonify([{
        'user_id': msg.Messages.user_id,
        'message': msg.Messages.content,
        'timestamp': msg.Messages.timestamp.isoformat(),
        'name': msg.name,  # From joined Users table
        'message_type': msg.Messages.message_type.value  # Get enum value
    } for msg in messages])

################# SOCKETIO #################

@socketio.on('connect')
@jwt_required()
def handle_connect():
    print("\n=== SocketIO connected ===")
    user_id = get_jwt_identity()
    print(f"User {user_id} connected")
    socketio.emit('connection_established', {'user_id': user_id})

@socketio.on('join_room')
@jwt_required()
def handle_join_room(data):
    print("\n=== SocketIO join_room called ===")
    user_id = get_jwt_identity()
    room_id = data['room_id']
    
    print(f"User {user_id} wants to join room {room_id}")
    
    # Check if user is a member of the room
    if Room_Users.query.filter_by(user_id=user_id, room_id=room_id).first():
        join_room(room_id)  # <-- This is the correct way to join a room
        emit('room_joined', {
            'room_id': room_id,
            'message': f'Successfully joined room {room_id}'
        }, room=room_id)
    else:
        emit('join_error', {
            'message': 'You are not a member of this room'
        })

# Leave room
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
        
        # Verify room membership
        if not Room_Users.query.filter_by(user_id=user_id, room_id=room_id).first():
            emit('message_error', {'message': 'Not authorized to send to this room'})
            return
        
        # Save message to database (optional)
        new_message = Messages(
            user_id=user_id,
            room_id=room_id,
            content=message_content,
            message_type= MessageType.TEXT
        )
        db.session.add(new_message)
        db.session.commit()
        
        # Broadcast to room
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



if __name__ == '__main__':
    app.run(debug=True)