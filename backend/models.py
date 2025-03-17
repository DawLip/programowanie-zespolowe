from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()

# Enum dla ról
class Role(Enum):
    USER = 0
    ADMIN = 1
    SUPERADMIN = 2

# Model użytkownika
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    role = db.Column(db.Enum(Role), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    facebook = db.Column(db.String(50), nullable=True)
    instagram = db.Column(db.String(50), nullable=True)
    linkedin = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(128), nullable=False)

    # Propozycja dodania daty utworzenia i aktualizacji
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.email}>'