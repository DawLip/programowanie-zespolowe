from flask import Flask, jsonify, request, abort, render_template, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, Users, Role
import bcrypt

app = Flask(__name__)

# Konfiguracja bazy danych SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Konfiguracja JWT
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

# Inicjalizacja bazy danych
db.init_app(app)

# Tworzenie tabel w bazie danych
with app.app_context():
    db.create_all()

# Strona główna z listą użytkowników
@app.route('/')
def index():
    users = Users.query.all()
    return render_template('index.html', users=users)

# Rejestracja nowego użytkownika
@app.route('/auth/register', methods=['POST'])
def register():
    # Pobieranie danych z formularza/JSON, choose one
    data = request.get_json()
    # data = request.form.get()
    email = data.get('email')
    password = data.get('password')
    name = "John"   # placeholder
    surname = "Doe" # placeholder

    if not email or not password:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
    
    # if email is taken
    if Users.query.filter_by(email=email).first():
        return jsonify({"status": "email is taken"}), 400
    
    # Hashowanie hasła
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Tworzenie nowego uzytkownika
    new_user = Users(email=email, password=hashed_password.decode('utf-8'), name=name, surname=surname)
    db.session.add(new_user)
    db.session.commit()

    # Tworzenie tokenu JWT
    access_token = create_access_token(identity=new_user.id)

    return jsonify({"status": "success", "access_token": access_token}), 200

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"status": "error", "message": "Missing email or password"}), 400

    # Wyszukanie użytkownika w bazie danych
    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    # Weryfikacja hasła
    if password == data.get('password'):
        access_token = create_access_token(identity=user.id)
        return jsonify({"status": "success", "access_token": access_token}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid email or password"}), 401
    
from flask import request, jsonify
from sqlalchemy import or_, and_

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
    
##############################  |
###Funkcje tylko do przykladu#  |
##############################  V


# Tworzenie nowego użytkownika
@app.route('/users', methods=['POST'])
def create_user():
    email = request.form.get('email')
    role = request.form.get('role')
    name = request.form.get('name')
    surname = request.form.get('surname')
    phone = request.form.get('phone')
    address = request.form.get('address')
    facebook = request.form.get('facebook')
    instagram = request.form.get('instagram')
    linkedin = request.form.get('linkedin')
    password = request.form.get('password')

    if not email or not role or not name or not surname or not password:
        abort(400, description="Missing required fields")

    try:
        role = Role(int(role))  # Konwersja roli na Enum
    except ValueError:
        abort(400, description="Invalid role")

    user = Users(
        email=email,
        role=role,
        name=name,
        surname=surname,
        phone=phone,
        address=address,
        facebook=facebook,
        instagram=instagram,
        linkedin=linkedin,
        password=password  # W praktyce hasło powinno być zahashowane!
    )
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

# Usuwanie użytkownika
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

# Formularz do aktualizacji użytkownika
@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = Users.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

# Aktualizacja użytkownika
@app.route('/users/<int:user_id>/update', methods=['POST'])
def update_user(user_id):
    user = Users.query.get_or_404(user_id)
    email = request.form.get('email')
    role = request.form.get('role')
    name = request.form.get('name')
    surname = request.form.get('surname')
    phone = request.form.get('phone')
    address = request.form.get('address')
    facebook = request.form.get('facebook')
    instagram = request.form.get('instagram')
    linkedin = request.form.get('linkedin')
    password = request.form.get('password')

    if email:
        user.email = email
    if role:
        try:
            user.role = Role(int(role))  # Konwersja roli na Enum
        except ValueError:
            abort(400, description="Invalid role")
    if name:
        user.name = name
    if surname:
        user.surname = surname
    if phone:
        user.phone = phone
    if address:
        user.address = address
    if facebook:
        user.facebook = facebook
    if instagram:
        user.instagram = instagram
    if linkedin:
        user.linkedin = linkedin
    if password:
        user.password = password  # W praktyce hasło powinno być zahashowane!

    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)