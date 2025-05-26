from flask import Flask, request, jsonify, session
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Requires Python 3.9+
from flask_cors import CORS
import json
import os
import jwt
from functools import wraps
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

JWT_SECRET = app.secret_key
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 1 * 60 * 60  # 1 hour

# CORS(app, supports_credentials=True, origins=lambda origin: True)

CORS(app)

# database
# SQLite config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mess_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class MessRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mess_choice = db.Column(db.String(50), nullable=False)
    plan_choice = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class RegistrationHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mess_choice = db.Column(db.String(50), nullable=False)
    plan_choice = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)    

# USERS + MESS_DATA + HISTORY files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, 'users.json')
MESS_DATA_FILE = os.path.join(BASE_DIR, 'mess_data.json')
HISTORY_FILE = os.path.join(BASE_DIR, 'history_data.json')

# Load users from file at startup
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
else:
    users = {}

# Load data from file at startup
if os.path.exists(MESS_DATA_FILE):
    with open(MESS_DATA_FILE, 'r') as f:
        registrations = json.load(f)
else:
    registrations = {}


# decorator to protect routes (replace session checks)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # JWT token sent in Authorization header: "Bearer <token>"
        auth_header = request.headers.get('Authorization')
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            current_user = payload['email']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired! Please login again.'}), 401
        except (jwt.InvalidTokenError, Exception):
            return jsonify({'message': 'Invalid token!'}), 401

        # Attach current_user to kwargs or global context as needed
        return f(current_user, *args, **kwargs)
    return decorated
    
# login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        # proceed with JWT token generation
        payload = {
            'email': email,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return jsonify({'message': 'Login successful', 'token': token}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

# sign up
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # add registration to users database
    # check if account exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Account already exists'}), 409

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Sign up successful'}), 200


# mess registration
@app.route('/register-mess', methods=['POST'])
@token_required
def register_mess(current_user):
    data = request.json
    mess = data.get('mess')
    plan = data.get('plan')

    if not mess or not plan:
        return jsonify({'message': 'Missing mess or plan selection'}), 400

    existing_registration = MessRegistration.query.filter_by(email=current_user).first()

    if existing_registration:
        existing_registration.mess_choice = mess
        existing_registration.plan_choice = plan
        existing_registration.timestamp = datetime.utcnow()
    else:
        new_registration = MessRegistration(email=current_user, mess_choice=mess, plan_choice=plan)
        db.session.add(new_registration)

    db.session.commit()

    # Save to history
    new_history = RegistrationHistory(
        email=current_user,
        mess_choice=mess,
        plan_choice=plan,
        timestamp=datetime.now(ZoneInfo("Asia/Kolkata")),
        status="registered"
    )
    db.session.add(new_history)
    db.session.commit()

    return jsonify({'message': 'Mess registration successful'})

# get email of current user
@app.route('/current-user', methods=['GET'])
@token_required
def current_user_route(current_user):
    return jsonify({'email': current_user}), 200

# get mess data of current user
@app.route('/mess_data', methods=['GET'])
@token_required
def get_mess_data(current_user):
    registration = MessRegistration.query.filter_by(email=current_user).first()
    if registration:
        return jsonify({
            'mess': registration.mess_choice,
            'plan': registration.plan_choice
        })
    else:
        return jsonify({"error": "User not registered"}), 404

@app.route('/unregister-user', methods=['GET'])
@token_required
def unregister_user(current_user):
    registration = MessRegistration.query.filter_by(email=current_user).first()

    if registration:
        db.session.delete(registration)
        db.session.commit()

        # Add to history
        new_history = RegistrationHistory(
            email=current_user,
            mess_choice="-",
            plan_choice="-",
            timestamp=datetime.now(ZoneInfo("Asia/Kolkata")),
            status="unregistered"
        )
        db.session.add(new_history)
        db.session.commit()

        return jsonify({"message": "User unregistered successfully"}), 200
    else:
        return jsonify({"error": "User not registered"}), 404

# history 
@app.route('/get-history', methods=['GET'])
@token_required
def get_history(current_user):
    history_data = RegistrationHistory.query.filter_by(email=current_user).order_by(RegistrationHistory.timestamp.desc()).all()
    user_history = []
    for entry in history_data:
        user_history.append({
            "email": entry.email,
            "mess": entry.mess_choice,
            "plan": entry.plan_choice,
            "timestamp": entry.timestamp.strftime("%d-%m-%Y %H:%M:%S"),
            "status": entry.status
        })
    return jsonify(user_history)

# backend page
@app.route('/')
def index():
    return "Backend is live!"


if __name__ == '__main__':
    app.run()