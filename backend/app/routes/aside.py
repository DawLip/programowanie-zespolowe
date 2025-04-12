from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Users, Messages, Room, Room_Users, RoomType, Friends
from sqlalchemy import desc, func

aside_bp = Blueprint('aside', __name__)

@aside_bp.route('/aside', methods=['GET'])
@jwt_required()
def get_aside():
    user_id = get_jwt_identity()
    current_user = Users.query.get(user_id)
    friends = []

    #Pobierz wszystkich znajomych (relacja mutual)
    friendships = Friends.query.filter(
        (Friends.user_id == user_id) | (Friends.friend_id == user_id)
    ).filter(Friends.status == 'accepted').all()
    
    for friendship in friendships:
        friend_id = friendship.friend_id if friendship.user_id == user_id else friendship.user_id
        friend = Users.query.get(friend_id)
        
        #Znajdź pokój czatu przez Room_Users
        room = Room.query.join(Room_Users, (Room.id == Room_Users.room_id))\
            .filter(
                Room_Users.user_id.in_([user_id, friend_id]),
                Room.type == RoomType.PRIVATE
            )\
            .group_by(Room.id)\
            .having(func.count(Room_Users.user_id) == 2)\
            .first()

        last_msg = Messages.query.filter_by(room_id=room.id).order_by(desc(Messages.timestamp)).first() if room else None
        
        friends.append({
            "id": friend.id,
            "roomId": room.id,
            "name": friend.name,
            "surname": friend.surname,
            "lastMessage": last_msg.content if last_msg else "",
            "lastMessageAuthor": Users.query.get(last_msg.user_id).name if last_msg else "",
            "isActive": friend.is_active
        })

    #Grupy
    groups = []
    group_rooms = Room.query.filter_by(type=RoomType.GROUP).join(Room_Users)\
        .filter(Room_Users.user_id == user_id).all()
        
    for room in group_rooms:
        last_msg = Messages.query.filter_by(room_id=room.id).order_by(desc(Messages.timestamp)).first()
        
        groups.append({
            "roomId": room.id,
            "name": room.name,
            "lastMessage": last_msg.content if last_msg else "",
            "lastMessageAuthor": Users.query.get(last_msg.user_id).name if last_msg else "",
            "isActive": True
        })

    return jsonify({"friends": friends, "groups": groups})