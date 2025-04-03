from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

# Initialize extensions without app first (important!)
db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    
    # Load configuration
    app.config.from_object('app.config.Config')
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.chat import chat_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(chat_bp, url_prefix='/api')
    
    # Register socket handlers
    from app.sockets import register_socket_handlers
    register_socket_handlers(socketio)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app