import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Role, Room, Room_Users, Messages, RoomType, Users, db

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/my-rooms', methods=['GET'])
@jwt_required()
def get_my_rooms():
    """
    Endpoint zwraca listę pokoi dla zalogowanego uzytkownika

    Args:
        None

    Returns:
        JSON odpowiedz z listą pokoi
    """
    try:
        user_id = get_jwt_identity()
        print("Decoded user_id from JWT:", user_id)
        
        rooms = Room.query.join(Room_Users).filter(Room_Users.user_id == user_id).all()
        print("SQL query executed. Found rooms:", [r.name for r in rooms])
        
        return jsonify({
            "status": "success",
            "rooms": [{"id": r.id, "name": r.name, "type": r.type.name if hasattr(r.type, 'name') else str(r.type)} for r in rooms]
        })
    except Exception as e:
        print("ERROR in my-rooms:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

@chat_bp.route('/rooms/<int:room_id>/messages', methods=['GET'])
@jwt_required()
def get_room_messages(room_id):
    """
    Endpoint zwraca listę wiadomości dla zalogowanego uzytkownika

    Args:
        room_id (int): Identyfikator pokoju

    Returns:
        JSON odpowiedz z listą wiadomości
    """
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
        'message_id': msg.Messages.id,
        'user_id': msg.Messages.user_id,
        'message': msg.Messages.content,
        'timestamp': msg.Messages.timestamp.isoformat(),
        'name': msg.name,  # From joined Users table
        'message_type': msg.Messages.message_type.value  # Get enum value
    } for msg in messages])
    
    
# Tworzenie Chatu Grupowego
@chat_bp.route('/rooms/create', methods=['POST'])
@jwt_required()
def create_room():
    """
    Edpoint dla tworzenia nowego pokoju

    Args:
        name: string (nazwa pokoju)

    Returns:
        json: {
            status: string ("success" or "error")
            message: string (optional)
            room_id: int
        }

    Error codes:
        400: Missing required fields
        400: Email is taken
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"status": "error", "message": "Missing room name"}), 400

    try:
        new_room = Room(
            type=RoomType.GROUP,
            name=data['name'],
            created_at=datetime.utcnow()
        )
        db.session.add(new_room)
        db.session.flush()

        # Add creator as OWNER
        db.session.add(Room_Users(
            room_id=new_room.id,
            user_id=current_user_id,
            role=Role.OWNER
        ))
        
        # Add members if provided
        if 'members' in data:
            for member_id in data['members']:
                if member_id != current_user_id:
                    db.session.add(Room_Users(
                        room_id=new_room.id,
                        user_id=member_id,
                        role=Role.USER
                    ))
        
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "room_id": new_room.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# Usuwanie czatu
@chat_bp.route('/rooms/<int:room_id>', methods=['DELETE'])
@jwt_required()
def delete_group_chat(room_id):
    """
    Endpoint dla usuwania pokoju

    Args:
        room_id: int (identyfikator pokoju)

    Returns:
        json: {
            status: string ("success" or "error")
            message: string (optional)
        }
    """
    current_user_id = get_jwt_identity()
    
    # Sprawdź uprawnienia 
    membership = Room_Users.query.filter_by(
        room_id=room_id,
        user_id=current_user_id,
        role=Role.OWNER
    ).first()
    
    if not membership:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
    
    try:
        # Usunięcie pokoju 
        room = Room.query.get(room_id)
        db.session.delete(room)
        db.session.commit()
        
        return jsonify({"status": "success", "message": "Chat deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# Dodawanie użytkowników do czatu
@chat_bp.route('/rooms/<int:room_id>/add-member', methods=['POST'])
@jwt_required()
def add_group_member(room_id):
    """
    Endpoint dla dodawania nowego uzytkownika do czatu grupowego

    Args:
        room_id (int): ID pokoju do którego dodawany jest uzytkownik

    Returns:
        json: {
            status (str): "success" or "error"
            message (str): Wiadomość o wyniku operacji
        }

    Error codes:
        403: Unauthorized if the current user is not an admin or owner.
        400: Missing user_id in the request or if the user is already in the group.
        500: Internal server error if unable to add the user.
    """

    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Sprawdź uprawnienia (admin lub owner)
    membership = Room_Users.query.filter_by(
        room_id=room_id,
        user_id=current_user_id
    ).first()
    
    if not membership or membership.role == Role.USER:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
    
    if not data or 'user_id' not in data:
        return jsonify({"status": "error", "message": "Missing user_id"}), 400
    
    try:
        # Sprawdź czy użytkownik już jest w grupie
        existing = Room_Users.query.filter_by(
            room_id=room_id,
            user_id=data['user_id']
        ).first()
        
        if existing:
            return jsonify({"status": "error", "message": "User already in group"}), 400
        
        # Dodaj użytkownika
        new_member = Room_Users(
            room_id=room_id,
            user_id=data['user_id'],
            role=Role.USER
        )
        db.session.add(new_member)
        db.session.commit()
        
        return jsonify({"status": "success", "message": "User added to group"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# Usuwanie użytkowników z czatu
@chat_bp.route('/rooms/<int:room_id>/remove-member', methods=['POST'])
@jwt_required()
def remove_group_member(room_id):
    """
    Endpoint do usuwania uzytkownikow z czatu

    Args:
        room_id (int): ID pokoju z którego usuwany jest uzytkownik

    Returns:
        json: {
            status (str): "success" or "error"
            message (str): Wiadomość o wyniku operacji
        }

    Error codes:
        403: Unauthorized if the current user is not a member or lacks permission to remove the target member.
        400: Missing user_id in the request or if attempting to remove the owner.
        500: Internal server error if unable to remove the user.

    Notes:
        - Admins and superadmins can remove any member except the owner.
        - Regular users can only remove themselves.
    """

    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Sprawdź uprawnienia (admin/superadmin może usuwać innych, user tylko siebie)
    requester_membership = Room_Users.query.filter_by(
        room_id=room_id,
        user_id=current_user_id
    ).first()
    
    if not requester_membership:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
    
    if not data or 'user_id' not in data:
        return jsonify({"status": "error", "message": "Missing user_id"}), 400
    
    # Superadmin nie może być usunięty
    target_membership = Room_Users.query.filter_by(
        room_id=room_id,
        user_id=data['user_id']
    ).first()
    
    if target_membership.role == Role.OWNER:
        return jsonify({"status": "error", "message": "Cannot remove owner"}), 400
    
    # Zwykły użytkownik może usunąć tylko siebie
    if requester_membership.role == Role.USER and current_user_id != data['user_id']:
        return jsonify({"status": "error", "message": "Can only remove yourself"}), 403
    
    try:
        db.session.delete(target_membership)
        db.session.commit()
        return jsonify({"status": "success", "message": "User removed from group"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# Zmiana uprawnień użytkownika
@chat_bp.route('/rooms/<int:room_id>/change-role', methods=['POST'])
@jwt_required()
def change_member_role(room_id):
    """
    Endpoint do zmiany uprawnień uzytkownikow

    Args:
        room_id (int): ID pokoju zródowego uzytkownika

    Returns:
        json: {
            status (str): "success" or "error"
            message (str): Wiadomość o wyniku operacji
        }

    Error codes:
        403: Unauthorized if the current user is not a superadmin.
        400: Missing user_id or new_role in the request, or if attempting to change the role of the superadmin.
        404: User not found in the group.
        500: Internal server error if unable to change the role.

    Notes:
        - Only superadmins can change the role of a member.
        - Regular users cannot change their own role.
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    print(f"Changing role in room {room_id} of user {data['user_id']} to {data['new_role']}")
    
    # Tylko superadmin może zmieniać role
    requester_membership = Room_Users.query.filter_by(
        room_id=room_id,
        user_id=current_user_id,
        role=Role.OWNER
    ).first()
    
    if not requester_membership:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
    
    if not data or 'user_id' not in data or 'new_role' not in data:
        return jsonify({"status": "error", "message": "Missing parameters"}), 400
    
    # Nie można zmienić roli superadmina
    if data['user_id'] == current_user_id:
        return jsonify({"status": "error", "message": "Cannot change your own role"}), 400
    
    try:
        target_membership = Room_Users.query.filter_by(
            room_id=room_id,
            user_id=data['user_id']
        ).first()
        
        if not target_membership:
            return jsonify({"status": "error", "message": "User not found in group"}), 404
        
        target_membership.role = Role(data['new_role'])
        db.session.commit()
        
        return jsonify({"status": "success", "message": "Role updated"}), 200
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid role"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# Pobieranie informacji o czacie
@chat_bp.route('/rooms/<int:room_id>', methods=['GET'])
@jwt_required()
def get_room_info(room_id):
    """
    Endpoint do pobierania informacji o czacie

    Args:
        room_id (int): ID pokoju

    Returns:
        json: {
            status (str): "success" or "error"
            room (dict): Informacje o czacie
            members (list): Lista członków czatu
        }

    Error codes:
        403: Unauthorized if the current user is not a member of the group.
        500: Internal server error if unable to fetch the room information.
    """
    current_user_id = get_jwt_identity()
    
    # Sprawdź czy użytkownik należy do czatu
    membership = Room_Users.query.filter_by(
        room_id=room_id,
        user_id=current_user_id
    ).first()
    
    if not membership:
        return jsonify({"status": "error", "message": "Not a member"}), 403
    
    try:
        room = Room.query.get(room_id)
        members = Room_Users.query.filter_by(room_id=room_id).all()
        
        return jsonify({
            "status": "success",
            "room": {
                "id": room.id,
                "name": room.name,
                "type": room.type.value,
                "created_at": room.created_at.isoformat()
            },
            "members": [{
                "user_id": m.user_id,
                "role": m.role.value,
                "joined_at": m.joined_at.isoformat()
            } for m in members]
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
# Zapisz zmiany w nazwie i opisie
@chat_bp.route('/rooms/<int:room_id>/save-changes', methods=['POST'])
@jwt_required()
def save_room_changes(room_id):
    """
    Endpoint do zapisywania zmian w nazwie i opisie czatu

    Args:
        room_id (int): ID pokoju

    Returns:
        json: {
            status (str): "success" or "error"
            message (str): Wiadomość o wyniku operacji
        }

    Error codes:
        403: Unauthorized if the current user is not a member of the group.
        400: Missing name or description in the request.
        500: Internal server error if unable to save the changes.
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Sprawdź uprawnienia (admin/superadmin)
    membership = Room_Users.query.filter_by(
        room_id=room_id,
        user_id=current_user_id
    ).first()
    
    if not membership or membership.role == Role.USER:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
    
    if not data or 'name' not in data or 'description' not in data:
        return jsonify({"status": "error", "message": "Missing parameters"}), 400
    
    try:
        room = Room.query.get(room_id)
        room.name = data['name']
        room.description = data['description']
        db.session.commit()
        
        return jsonify({"status": "success", "message": "Room updated"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500