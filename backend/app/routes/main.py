from flask import Blueprint, render_template
from app.models import Users

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    print("\n=== / called ===")
    users = Users.query.all()
    return render_template('chat.html', users=users)