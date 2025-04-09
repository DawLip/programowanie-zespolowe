from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Users, Messages, Room, Room_Users, Friends
from sqlalchemy import desc, func

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    user_id = get_jwt_identity()
    
    #Pobierz zaproszenia
    invitations = Users.query.join(Friends, Friends.user_id == Users.id)\
        .filter(Friends.friend_id == user_id, Friends.status == 'pending').all()
    
    #Ostatnie czaty
    last_chats = []
    private_rooms = Room.query.join(Room_Users).filter(
        Room_Users.user_id == user_id,
        Room.type == 'PRIVATE'
    ).all()
    
    for room in private_rooms:
        last_message = Messages.query.filter_by(room_id=room.id)\
            .order_by(desc(Messages.timestamp)).first()
        if last_message:
            last_chats.append({
                'userId': room.other_user.id,
                'name': room.other_user.name,
                'surname': room.other_user.surname,
                'messages': [{
                    'messageAuthor': last_message.user.name,
                    'message': last_message.content
                }],
                'isActive': room.other_user.is_active
            })

    #Grupy
    groups = []
    group_rooms = Room.query.filter_by(type='GROUP').join(Room_Users)\
        .filter(Room_Users.user_id == user_id).all()
        
    for group in group_rooms:
        group_messages = Messages.query.filter_by(room_id=group.id)\
            .order_by(desc(Messages.timestamp)).limit(3).all()
        groups.append({
            'groupId': group.id,
            'name': group.name,
            'messages': [{
                'messageAuthor': msg.user.name,
                'message': msg.content
            } for msg in group_messages],
            'isActive': True
        })

    #Sugerowani znajomi
    may_know = Users.query.filter(
        ~Users.friends.any(user_id=user_id),
        Users.id != user_id
    ).limit(5).all()

    return jsonify({
        'invitations': [{
            'id': u.id,
            'name': u.name,
            'surname': u.surname,
            'isActive': u.is_active
        } for u in invitations],
        'lastChats': last_chats,
        'groups': groups,
        'mayKnow': [{
            'id': u.id,
            'name': u.name,
            'surname': u.surname,
            'isActive': u.is_active
        } for u in may_know]
    })