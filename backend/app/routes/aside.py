from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Users, Messages, Room, Room_Users, RoomType, Friends
from sqlalchemy import desc, func
from sqlalchemy.orm import aliased


aside_bp = Blueprint('aside', __name__)

@aside_bp.route('/aside', methods=['GET'])
@jwt_required()
def get_aside():
    """
    Endpoint zwraca informacje o znajomych i grupach, z ktorymi jest powiazany uzytkownik.
    
    Returns:
        friends - lista znajomych, kazdy znajomy to:
            id - id znajomego
            roomId - id prywatnego pokoju, w ktorym uzytkownik rozmawia z znajomym
            name - imie znajomego
            surname - nazwisko znajomego
            lastMessage - tresc ostatniej wiadomosci w prywatnym pokoju
            lastMessageAuthor - autor ostatniej wiadomosci w prywatnym pokoju
            isActive - czy znajomy jest aktywny
        groups - lista grup, kazda grupa to:
            roomId - id pokoju grupowego
            name - nazwa pokoju
            lastMessage - tresc ostatniej wiadomosci w pokoju
            lastMessageAuthor - autor ostatniej wiadomosci w pokoju
            isActive - czy grupa jest aktywna
    """
    print("\n=== /aside called ===")
    user_id = get_jwt_identity()
    current_user = Users.query.get(user_id)
    friends = []

    #Pobierz wszystkich znajomych (relacja mutual)
    friendships = Friends.query.filter(
        (Friends.user_id == user_id) | (Friends.friend_id == user_id)
    ).filter(Friends.status == 'accepted').all()
    print("=== group_rooms ===")    
    print(friendships)
    print("user id: " + str(user_id))
    
    for friendship in friendships:
        friend_id = friendship.friend_id if int(friendship.user_id) == int(user_id) else friendship.user_id
        print(f"=== friend_id === {friend_id}")
        friend = Users.query.get(friend_id)
        
        ru1 = aliased(Room_Users)
        ru2 = aliased(Room_Users)
        
        room = Room.query\
            .join(ru1, ru1.room_id == Room.id)\
            .join(ru2, ru2.room_id == Room.id)\
            .filter(
                ru1.user_id == user_id,
                ru2.user_id == friend_id,
                Room.type == RoomType.PRIVATE
            )\
            .first()
        print(room)

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