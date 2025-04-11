from enum import Enum
from datetime import datetime
from app import db

class MessageType(Enum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    VIDEO = 'VIDEO'
    FILE = 'FILE'

class RoomType(Enum):
    PRIVATE = 'PRIVATE'
    GROUP = 'GROUP'

class Role(Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'
    SUPERADMIN = 'SUPERADMIN'

# Relacja znajomych
class Friends(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('pending', 'accepted', 'declined'), default='pending')
    
# Model użytkownika
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)  #in register
    name = db.Column(db.String(50), nullable=False)                             #in register
    surname = db.Column(db.String(50), nullable=False)                          #in register
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    facebook = db.Column(db.String(50), nullable=True)
    instagram = db.Column(db.String(50), nullable=True)
    linkedin = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(128), nullable=False)                        #in register
    is_active = db.Column(db.Boolean, default=True)

    # Propozycja dodania daty utworzenia i aktualizacji
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relacja friends
    friends = db.relationship(
        'Users',
        secondary='friends',
        primaryjoin=(id == Friends.user_id),
        secondaryjoin=(id == Friends.friend_id),
        backref='friends_back',
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<User {self.email}>'
    
# Model pokoju
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Enum(RoomType), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacje
    messages = db.relationship('Messages', backref='room', lazy=True, cascade='all, delete-orphan')
    members = db.relationship('Room_Users', backref='room', lazy=True, cascade='all, delete-orphan')

# Członkostwo w pokoju z rolą
class Room_Users(db.Model):
    __tablename__ = 'room_users'
    room_id = db.Column(db.Integer, db.ForeignKey('room.id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role = db.Column(db.Enum(Role), default=Role.USER, nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_user_rooms', 'user_id', 'room_id'),  # Szybkie wyszukiwanie pokojów użytkownika
    )

# Model wiadomości
class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id', ondelete='CASCADE'))
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.Enum(MessageType), default=MessageType.TEXT, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        db.Index('idx_room_timestamp', 'room_id', 'timestamp'),  # Szybkie pobieranie historii
    )