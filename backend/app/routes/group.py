from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Users, Room, Room_Users

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
        'members': [{
            'id': m.id,
            'name': m.name,
            'role': Room_Users.query.filter_by(room_id=group_id, user_id=m.id).first().role.value
        } for m in members]
    })