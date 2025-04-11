from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Users, Messages, Room, Room_Users, Friends, RoomType
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
        Room.type == RoomType.PRIVATE
    ).all()
    
    for room in private_rooms:
        #Znajdź drugiego użytkownika w pokoju
        other_user = Users.query.join(Room_Users).filter(
            Room_Users.room_id == room.id,
            Users.id != user_id
        ).first()
        
        last_message = Messages.query.filter_by(room_id=room.id)\
            .order_by(Messages.timestamp.desc()).first()
        
        if last_message and other_user:
            author = Users.query.get(last_message.user_id)  #Pobierz autora przez user_id
            last_chats.append({
                "userId": other_user.id,
                "name": other_user.name,
                "surname": other_user.surname,
                "messages": [{
                    "messageAuthor": author.name if author else "Unknown",
                    "message": last_message.content
                }],
                "isActive": other_user.is_active
            })

    #Grupy
    groups = []
    group_rooms = Room.query.filter_by(type=RoomType.GROUP).join(Room_Users)\
        .filter(Room_Users.user_id == user_id).all()
        
    for group in group_rooms:
        group_messages = Messages.query.filter_by(room_id=group.id)\
            .order_by(desc(Messages.timestamp)).limit(3).all()
        
        messages_data = []
        for msg in group_messages:
            author = Users.query.get(msg.user_id)  #Pobierz autora przez user_id
            messages_data.append({
                "messageAuthor": author.name if author else "Unknown",
                "message": msg.content
            })
        
        groups.append({
            "groupId": group.id,
            "name": group.name,
            "messages": messages_data,
            "isActive": True
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