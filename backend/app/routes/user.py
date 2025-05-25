import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Users, Friends, db
from sqlalchemy import or_, and_
from flask_cors import cross_origin
from app.models import Room, Room_Users, Messages, Users, db, RoomType, Role
from datetime import datetime


user_bp = Blueprint('user', __name__)

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    """
    Endpoint do pobierania informacji o uzytkowniku

    Args:
        user_id (int): ID uzytkownika

    Returns:
        json: {
            status (str): "success" or "error"
            user (dict): informacje o uzytkowniku
        }

    Error codes:
        404: Not Found if the user does not exist.
    """
    
    print("tesfdsagfdgdfdgsfsdgfdgsf")
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"status": "error"}), 404

    # Pobierz znajomych w obie strony (relacja mutual)
    friends_query = db.session.query(Friends).filter(
        (Friends.user_id == user_id) | (Friends.friend_id == user_id)
    )

    friends_ids = []
    for friendship in friends_query.all():
        if friendship.user_id == user_id:
            friends_ids.append(friendship.friend_id)
        else:
            friends_ids.append(friendship.user_id)

    friends_ids = list(set(friends_ids))
    if user_id in friends_ids:
        friends_ids.remove(user_id)

    #print user information
    print(f"User: {user.name} {user.surname}"
          f"email: {user.email}\n phone: {user.phone}\n"
          f"address: {user.address}\n facebook: {user.facebook}\n"
          f"instagram: {user.instagram}\n linkedin: {user.linkedin}\n"
          f"About: {user.about_me}\n")

    return jsonify({
        "id": user.id,
        "password": user.password,
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
        "phone": user.phone,
        "address": user.address,
        "facebook": user.facebook,
        "instagram": user.instagram,
        "linkedin": user.linkedin,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        "friends": friends_ids
    }), 200

@user_bp.route('/<int:user_id>', methods=['POST'])
@jwt_required()
def update_user_by_id(user_id):
    """
    Endpoint do aktualizacji informacji o uzytkowniku

    Args:
        user_id (int): ID uzytkownika

    Returns:
        json: {
            status (str): "success" or "error"
        }

    Error codes:
        404: Not Found if the user does not exist.
        400: Missing data in the request.
        500: Internal server error if unable to update the user.
    """
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"status": "error"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"status": "error"}), 400

    user.name = data.get('name', user.name)
    user.surname = data.get('surname', user.surname)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)
    user.phone = data.get('phone', user.phone)
    user.address = data.get('address', user.address)
    user.facebook = data.get('facebook', user.facebook)
    user.instagram = data.get('instagram', user.instagram)
    user.linkedin = data.get('linkedin', user.linkedin)
    user.about_me = data.get('About Me', user.about_me)
    
    try:
        db.session.commit()
        return jsonify({"status": "ok"}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"status": "error"}), 500

@user_bp.route('/search', methods=['GET'])
def search_users():
    """
    Endpoint do wyszukiwania uzytkownikow

    Args:
        query (str): query to search for

    Returns:
        json: {
            status (str): "success" or "error"
            count (int): number of found users
            users (list): list of found users, each containing id, name, and surname
        }

    Error codes:
        400: Missing query parameter or query too short.
        500: Internal server error if unable to search users.
    """
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
        
@user_bp.route('/invite/<int:user_id>', methods=['POST'])
@jwt_required()
def inviteUser(user_id):
    """
    Endpoint do wysyłania zaproszeń do użytkowników

    Args:
        user_id (int): ID użytkownika, do którego wysyłane jest zaproszenie

    Returns:
        json: {
            status (str): "success" or "error"
            message (str): Wiadomość o wyniku operacji
        }

    Error codes:
        400: Cannot invite yourself or invitation already exists.
        500: Internal server error if unable to send the invitation.
    """

    current_user_id = get_jwt_identity()
    if current_user_id == user_id:
        return jsonify({"status": "error", "message": "Cannot invite yourself"}), 400

    # Sprawdź, czy zaproszenie już istnieje
    existing_invite = Friends.query.filter(
        or_(
            and_(Friends.user_id == current_user_id, Friends.friend_id == user_id),
            and_(Friends.user_id == user_id, Friends.friend_id == current_user_id)
        )
    ).first()

    if existing_invite:
        return jsonify({"status": "error", "message": "Invitation already exists"}), 400

    # Dodaj zaproszenie
    new_invite = Friends(user_id=current_user_id, friend_id=user_id)
    db.session.add(new_invite)
    db.session.commit()

    return jsonify({"status": "ok", "message": "Invitation sent"}), 200

@user_bp.route('/invitation-accept/<int:user_id>', methods=['POST'])
@jwt_required()
def accept_invite(user_id):
    """
    Endpoint do akceptacji zaproszenia do znajomych obecnego uzytkownika i innego

    Args:
        user_id (int): Id uzytkownika, ktory otrzymal zaproszenie

    Returns:
        json: {
            status (str): "success" or "error"
            message (str): Wiadomość o wyniku operacji
        }

    Error codes:
        400: No invitation found or internal server error if unable to accept the invitation.
    """

    current_user_id = get_jwt_identity()

    # Sprawdź, czy zaproszenie istnieje
    existing_invite = Friends.query.filter(
        or_(
            and_(Friends.user_id == current_user_id, Friends.friend_id == user_id),
            and_(Friends.user_id == user_id, Friends.friend_id == current_user_id)
        )
    ).first()

    if not existing_invite:
        return jsonify({"status": "error", "message": "No invitation found"}), 400

    # Usuń zaproszenie
    db.session.delete(existing_invite)

    # Dodaj znajomego
    new_friend = Friends(user_id=current_user_id, friend_id=user_id, status='accepted')
    db.session.add(new_friend)
    db.session.commit()
    
    new_room = Room(
        type=RoomType.PRIVATE,
        name="PRIVATE",
        created_at=datetime.utcnow()
    )
    db.session.add(new_room)
    db.session.flush()
    
    db.session.add(Room_Users(
        room_id=new_room.id,
        user_id=current_user_id,
        role=Role.USER
    ))
    
    db.session.add(Room_Users(
        room_id=new_room.id,
        user_id=user_id,
        role=Role.USER
    ))
    db.session.commit()

    return jsonify({"status": "ok", "message": "Invitation accepted"}), 200

@user_bp.route('/invitation-decline/<int:user_id>', methods=['POST'])
@jwt_required()
def decline_invite(user_id):
    """
    Endpoint do odrzucenia zaproszenia do znajomych obecnego uzytkownika i innego

    Args:
        user_id (int): Id uzytkownika, ktory otrzymal zaproszenie

    Returns:
        json: {
            status (str): "success" or "error"
            message (str): Wiadomość o wyniku operacji
        }

    Error codes:
        400: No invitation found or internal server error if unable to accept the invitation.
    """
    current_user_id = get_jwt_identity()

    # Sprawdź, czy zaproszenie istnieje
    existing_invite = Friends.query.filter(
        or_(
            and_(Friends.user_id == current_user_id, Friends.friend_id == user_id),
            and_(Friends.user_id == user_id, Friends.friend_id == current_user_id)
        )
    ).first()

    if not existing_invite:
        return jsonify({"status": "error", "message": "No invitation found"}), 400

    # Usuń zaproszenie
    db.session.delete(existing_invite)
    db.session.commit()

    return jsonify({"status": "ok", "message": "Invitation declined"}), 200

PROFILE_PICTURES_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'utils', 'profilep')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DEFAULT_PROFILE_PICTURE = 'default.jpg'

# Utwórz folder jeśli nie istnieje
os.makedirs(PROFILE_PICTURES_DIR, exist_ok=True)
def allowed_file(filename):
    """
    Funkcja pomocnicza do sprawdzenia, czy plik ma prawidłowy format.

    Args:
        filename (str): Nazwa pliku.

    Returns:
        bool: True jeśli plik ma prawidłowy format, w przeciwnym przypadku False.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route('/<int:user_id>/profile-picture', methods=['POST'])
@jwt_required()
def upload_profile_picture(user_id):
    # Weryfikacja użytkownika
    """
    Endpoint do uploadu zdjęcia profilowego

    Args:
        user_id (int): ID uzytkownika, ktoremu przypisujemy nowe zdjęcie

    Returns:
        json: {
            status (str): "success" or "error"
            message (str): Wiadomość o wyniku operacji
        }

    Error codes:
        403: Unauthorized if the current user is not the same as the user_id.
        400: No file part or invalid file type.
    """
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    # Sprawdzenie czy przesłano plik
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Usunięcie starego zdjęcia jeśli istnieje
        for ext in ALLOWED_EXTENSIONS:
            old_path = os.path.join(PROFILE_PICTURES_DIR, f'{user_id}.{ext}')
            if os.path.exists(old_path):
                os.remove(old_path)

        # Zapisanie nowego zdjęcia
        filename = f"{user_id}.{file.filename.rsplit('.', 1)[1].lower()}"
        filepath = os.path.join(PROFILE_PICTURES_DIR, filename)
        file.save(filepath)
        return jsonify({"status": "ok", "message": "File uploaded successfully"}), 200

    return jsonify({"status": "error", "message": "Invalid file type"}), 400

@user_bp.route('/<int:user_id>/profile-picture', methods=['GET'])
def get_profile_picture(user_id):
    # Sprawdzenie istniejącego pliki
    """
    Endpoint do pobierania zdjęcia profilowego użytkownika

    Args:
        user_id (int): ID użytkownika

    Returns:
        File: zdjęcie profilowe użytkownika lub domyślne zdjęcie
    """
    for ext in ALLOWED_EXTENSIONS:
        filename = f"{user_id}.{ext}"
        if os.path.isfile(os.path.join(PROFILE_PICTURES_DIR, filename)):
            return send_from_directory(PROFILE_PICTURES_DIR, filename)
        
    # Zwróć domyślne zdjęcie jeśli nie znaleziono
    return send_from_directory(PROFILE_PICTURES_DIR, DEFAULT_PROFILE_PICTURE)