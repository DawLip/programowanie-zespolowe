from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Users, Friends, db
from sqlalchemy import or_, and_

user_bp = Blueprint('user', __name__)

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
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