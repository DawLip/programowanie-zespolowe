from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import Users, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
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

@auth_bp.route('/auth/login', methods=['POST'])
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