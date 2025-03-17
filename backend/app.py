from flask import Flask, jsonify, request, abort, render_template, redirect, url_for
from models import db, Users, Role

app = Flask(__name__)

# Konfiguracja bazy danych SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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