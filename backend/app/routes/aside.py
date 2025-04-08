from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Users, Messages, Room, Room_Users
from sqlalchemy import desc

aside_bp = Blueprint('aside', __name__)

@aside_bp.route('/aside', methods=['GET'])
@jwt_required()
def get_aside():
    user_id = get_jwt_identity()
    
    #Znajomi z ostatnią wiadomością
    friends = []
    for friend in Users.query.get(user_id).friends:
        room = Room.query.filter(
            ((Room.user1_id == user_id) & (Room.user2_id == friend.id)) |
            ((Room.user1_id == friend.id) & (Room.user2_id == user_id))
        ).first()
        
        last_msg = Messages.query.filter_by(room_id=room.id)\
            .order_by(desc(Messages.timestamp)).first() if room else None
        
        friends.append({
            'name': friend.name,
            'surname': friend.surname,
            'lastMessage': last_msg.content if last_msg else '',
            'lastMessageAuthor': last_msg.user.name if last_msg else '',
            'isActive': friend.is_active
        })

    #Grupy z ostatnią wiadomością
    groups = []
    for room in Room.query.filter_by(type='GROUP').join(Room_Users)\
        .filter(Room_Users.user_id == user_id).all():
        
        last_msg = Messages.query.filter_by(room_id=room.id)\
            .order_by(desc(Messages.timestamp)).first()
            
        groups.append({
            'name': room.name,
            'lastMessage': last_msg.content if last_msg else '',
            'lastMessageAuthor': last_msg.user.name if last_msg else '',
            'isActive': True
        })

    return jsonify({
        'friends': friends,
        'groups': groups
    })