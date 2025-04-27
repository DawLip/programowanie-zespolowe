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
          f"instagram: {user.instagram}\n linkedin: {user.linkedin}\n")

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
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"status": "error"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"status": "error"}), 400

    user.name = data.get('name', user.name)
    user.surname = data.get('surname', user.surname)
    user.email = data.get('email', user.email)
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