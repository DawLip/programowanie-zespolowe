from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from backend.app.models import db, Users, Messages, Room, Room_Users, MessageType
from flask_socketio import SocketIO
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_
from backend.app.sockets import register_socket_handlers

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
jwt = JWTManager(app)
db.init_app(app)
socketio = SocketIO(app)

# Register socket handlers
register_socket_handlers(socketio)

# Create database tables
with app.app_context():
    db.create_all()
    Session = sessionmaker(bind=db.engine)
    session = Session()

# Strona główna z listą użytkowników
@app.route('/')
def index():
    users = Users.query.all()
    return render_template('chat.html', users=users)

# Rejestracja nowego użytkownika
@app.route('/auth/register', methods=['POST'])
def register():
    # Pobieranie danych z formularza/JSON, choose one
    data = request.get_json()
    # data = request.form.get()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    surname = data.get('surname')

    if not email or not password:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
    
    # if email is taken
    if Users.query.filter_by(email=email).first():
        return jsonify({"status": "email is taken"}), 400
    
    # Hashowanie hasła
    # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Tworzenie nowego uzytkownika
    new_user = Users(email=email, password=password, name=name, surname=surname)
    # new_user = Users(email=email, password=hashed_password.decode('utf-8'), name=name, surname=surname)
    db.session.add(new_user)
    db.session.commit()

    # Tworzenie tokenu JWT
    access_token = create_access_token(identity=new_user.id)

    return jsonify({"status": "success", "access_token": access_token}), 200

# Logowanie
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"status": "error", "message": "Missing email or password"}), 400

    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    # Verify password - IMPORTANT: In production, use proper password hashing!
    if password == user.password:  # Changed from data.get('password')
        # Ensure identity is a string
        access_token = create_access_token(identity=str(user.id))  # Convert to string
        return jsonify({
            "status": "success",
            "access_token": access_token,
            # "user_id": user.id  # For debugging
        }), 200
    else:
        return jsonify({"status": "error", "message": "Invalid email or password"}), 401

@app.route('/users/search', methods=['GET'])
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

# Zwraca dane użytkownika po ID, wymaga autoryzacji JWT
@app.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"status": "error"}), 404

    # Serializacja znajomych
    friends = [{
        "id": f.id
    } for f in user.friends] if hasattr(user, 'friends') else []

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
        "friends": friends
    }), 200


# Aktualizuje dane użytkownika po ID, wymaga JWT
@app.route('/user/<int:user_id>', methods=['POST'])
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
    
#########################################################
####################  NIE DZIAŁA :( #####################
#########################################################

# Tworzenie Chatu Grupowego
@app.route('/api/rooms/create', methods=['POST'])
@jwt_required()
def create_room():
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

        # Add creator as SUPERADMIN
        db.session.add(Room_Users(
            room_id=new_room.id,
            user_id=current_user_id,
            role=Role.SUPERADMIN
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
@app.route('/api/rooms/<int:room_id>', methods=['DELETE'])
@jwt_required()
def delete_group_chat(room_id):
    current_user_id = get_jwt_identity()
    
    # Sprawdź uprawnienia (tylko superadmin może usunąć)
    membership = Room_Users.query.filter_by(
        room_id=room_id,
        user_id=current_user_id,
        role=Role.SUPERADMIN
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
@app.route('/api/rooms/<int:room_id>/add-member', methods=['POST'])
@jwt_required()
def add_group_member(room_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Sprawdź uprawnienia (admin lub superadmin)
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
@app.route('/api/rooms/<int:room_id>/remove-member', methods=['POST'])
@jwt_required()
def remove_group_member(room_id):
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
    
    if target_membership.role == Role.SUPERADMIN:
        return jsonify({"status": "error", "message": "Cannot remove superadmin"}), 400
    
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
@app.route('/api/rooms/<int:room_id>/change-role', methods=['POST'])
@jwt_required()
def change_member_role(room_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Tylko superadmin może zmieniać role
    requester_membership = Room_Users.query.filter_by(
        room_id=room_id,
        user_id=current_user_id,
        role=Role.SUPERADMIN
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
@app.route('/api/rooms/<int:room_id>', methods=['GET'])
@jwt_required()
def get_room_info(room_id):
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
    
    
#########################################################
#######################  Dotąd ##########################
#########################################################
    
################# Bonus Endpoints #################

@app.route('/api/my-rooms', methods=['GET'])
@jwt_required()
def get_my_rooms():
    print("\n=== /api/my-rooms called ===")
    # print("Request headers:", dict(request.headers))  # Verify Authorization header
    
    try:
        user_id = get_jwt_identity()
        print("Decoded user_id from JWT:", user_id)
        
        rooms = Room.query.join(Room_Users).filter(Room_Users.user_id == user_id).all()
        print("SQL query executed. Found rooms:", [r.name for r in rooms])
        
        return jsonify({
            "status": "success",
            "rooms": [{"id": r.id, "name": r.name} for r in rooms]
        })
    except Exception as e:
        print("ERROR in my-rooms:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/api/rooms/<int:room_id>/messages', methods=['GET'])
@jwt_required()
def get_room_messages(room_id):
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
        'user_id': msg.Messages.user_id,
        'message': msg.Messages.content,
        'timestamp': msg.Messages.timestamp.isoformat(),
        'name': msg.name,  # From joined Users table
        'message_type': msg.Messages.message_type.value  # Get enum value
    } for msg in messages])




if __name__ == '__main__':
    app.run(debug=True)