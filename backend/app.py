from flask import Flask, jsonify, request, abort, render_template, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, Users, Role, Messages
from flask_socketio import SocketIO
from sqlalchemy.orm import sessionmaker
import bcrypt

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

    # Wyszukanie użytkownika w bazie danych
    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    # Weryfikacja hasła
    if password == data.get('password'):
        access_token = create_access_token(identity=user.id)
        return jsonify({"status": "success", "access_token": access_token}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid email or password"}), 401

# Obsługa połaczenia
@socketio.on('connect')
def handle_connect():
    user_id = get_jwt_identity()
    socketio.emit('user_connected', user_id, broadcast=True)

# Obsługa wiadomości
@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)
    # socketio.emit('message', data, broadcast=True)

# Obsługa pokojów
@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    socketio.join_room(room)
    socketio.emit('message', f'User joined room {room}', room=room)

# Obsługa wysyłania wiadomości
@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    message = data['message']
    user_id = get_jwt_identity()
    
    new_message = Messages(user_id=user_id, room=room, content=message)
    db.session.add(new_message)
    db.session.commit()
    
    socketio.emit('message', message, room=room)

if __name__ == '__main__':
    app.run(debug=True)