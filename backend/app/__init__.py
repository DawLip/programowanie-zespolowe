from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_cors import CORS

# Initialize extensions without app first (important!)
db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")

def create_app():
    """
    Funkcja tworz ca  aplikacj  Flask oraz inicjalizuje wszystkie niezb dne
    rozszerzenia i blueprinty. Zwraca gotow  aplikacj  Flask.

    Returns:
        app (Flask): gotowa aplikacja Flask
    """
    app = Flask(__name__)
    CORS(app)
    
    # Load configuration
    app.config.from_object('app.config.Config')
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    
    socketio.init_app(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.chat import chat_bp
    from .routes.dashboard import dashboard_bp
    from .routes.aside import aside_bp
    from .routes.group import group_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(aside_bp)
    app.register_blueprint(group_bp)
    
    # Register socket handlers
    from app.sockets import register_socket_handlers
    register_socket_handlers(socketio)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app