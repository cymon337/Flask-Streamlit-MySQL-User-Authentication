from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')

# CONNECT TO MySQL DB
username = os.getenv('MYSQL_USERNAME', 'flask')
password = os.getenv('MYSQL_PASSWORD', 'flask')
host = os.getenv('MYSQL_HOST', '192.168.111.100')
dbname = os.getenv('MYSQL_DBNAME', 'FLASK')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}/{dbname}'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/register', methods=["POST"])
def register():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    
    # Check if user already exists
    if user:
        return jsonify({"message": "Email already registered"}), 400

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=8)
    new_user = User(email=data['email'], name=data['name'], password=hashed_password)
    
    db.session.add(new_user)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify({"message": "Registration failed"}), 500

    return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/logout', methods=["GET"])
def logout():
    logout_user()
    return jsonify({"message": "Logged out"}), 200

@app.route('/')
def home():
    return 'Flask is running!'

if __name__ == "__main__":
    app.run(debug=True)
