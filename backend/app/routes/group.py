from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Users, Room, Room_Users, RoomType, db
from datetime import datetime

group_bp = Blueprint('group', __name__)

@group_bp.route('/group/<int:group_id>', methods=['GET'])
@jwt_required()
def get_group(group_id):
    user_id = get_jwt_identity()
    
    if not Room_Users.query.filter_by(user_id=user_id, room_id=group_id).first():
        return jsonify({'error': 'Unauthorized'}), 403
        
    group = Room.query.get(group_id)
    members = Users.query.join(Room_Users).filter(Room_Users.room_id == group_id).all()
    
    return jsonify({
        'id': group.id,
        'name': group.name,
        'type': group.type.value,
        'description': group.description,
        'members': [{
            'id': m.id,
            'name': m.name,
            'surname': m.surname,
            'role': Room_Users.query.filter_by(room_id=group_id, user_id=m.id).first().role.value
        } for m in members]
    })


@group_bp.route('/group/new', methods=['POST'])
@jwt_required()
def create_group():
    data = request.get_json()
    #create group
    new_group = Room(
        type=RoomType.GROUP,
        name=data['name'],
        description=data['description'],
        created_at=datetime.utcnow()
    )
    db.session.add(new_group)
    db.session.commit()

    #Add self as admin
    user_id = get_jwt_identity()
    db.session.add(Room_Users(
        room_id=new_group.id,
        user_id=user_id,
        role='OWNER'
    ))
    db.session.commit()
    #Add members

    #Get group id
    group_id = new_group.id

    return jsonify({"groupId": group_id,"status": "ok"}), 200