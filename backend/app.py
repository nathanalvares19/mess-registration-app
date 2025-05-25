from flask import Flask, request, jsonify, session
from datetime import datetime, timedelta
from flask_cors import CORS
import json
import os

app = Flask(__name__)
# app.secret_key = 'your_secret_key_here'

# CORS(app)
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['SESSION_COOKIE_SECURE'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# CORS(app, supports_credentials=True, origins=["https://mess-registration-app-neon.vercel.app"])
CORS(app, supports_credentials=True)

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

# login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if email in users and users[email] == password:
        session['user'] = email
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

# sign up
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # add registration to users database
    # check if account exists
    if email in users:
        return jsonify({'message': 'Account already exists'}), 409
    else:
        users[email] = password
        # Save updated users to file
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f)
        return jsonify({'message': 'Sign up successful'}), 200

# mess registration
@app.route('/register-mess', methods=['POST'])
def register_mess():
    if 'user' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.json
    mess = data.get('mess')
    plan = data.get('plan')

    if not mess or not plan:
        return jsonify({'message': 'Missing mess or plan selection'}), 400

    else:
        user_email = session['user']

        registrations[user_email] = {
            'mess': mess,
            'plan': plan
        }

        # Save updated users to file
        with open(MESS_DATA_FILE, 'w') as f:
            json.dump(registrations, f)

    # Save to history
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    history_entry = {
        "email": session["user"],
        "mess": mess,
        "plan": plan,
        "timestamp": timestamp,
        "status": "registered"
    }

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history_data = json.load(f)
    else:
        history_data = []

    history_data.append(history_entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history_data, f, indent=2)

        # print(f"Registered {user_email} for mess {mess} with plan {plan}")

    return jsonify({'message': 'Mess registration successful'})

# get email of current user
@app.route('/current-user', methods=['GET'])
def current_user():
    if 'user' in session:
        return jsonify({'email': session['user']}), 200
    else:
        return jsonify({'email': None}), 401

# get mess data of current user
@app.route('/mess_data', methods=['GET'])
def get_mess_data():
    email = session['user']
    if os.path.exists(MESS_DATA_FILE):
        with open(MESS_DATA_FILE, 'r') as f:
            data = json.load(f)
            if email in data:
                return jsonify(data[email])
            else:
                return jsonify({"error": "User not registered"}), 404

    else:
        return jsonify({"error": "File not found"}), 404

# unregister user
@app.route('/unregister-user', methods=['GET'])
def unregister_user():
    email = session.get('user')
    if not email:
        return jsonify({"error": "Unauthorized"}), 401

    if os.path.exists(MESS_DATA_FILE):
        with open(MESS_DATA_FILE, 'r') as f:
            data = json.load(f)

        if email in data:
            del data[email]  # Remove the user data

            # Save the updated file
            with open(MESS_DATA_FILE, 'w') as f:
                json.dump(data, f)

            # Save to history
            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            history_entry = {
                "email": email,
                "mess": "-",
                "plan": "-",
                "timestamp": timestamp,
                "status": "unregistered"
            }

            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, "r") as f:
                    history_data = json.load(f)
            else:
                history_data = []

            history_data.append(history_entry)

            with open(HISTORY_FILE, "w") as f:
                json.dump(history_data, f, indent=2)

            return jsonify({"message": "User unregistered successfully"}), 200
        else:
            return jsonify({"error": "User not registered"}), 404
    else:
        return jsonify({"error": "File not found"}), 404



# history 
@app.route('/get-history', methods=['GET'])
def get_history():
    email = session.get('user')
    if not email:
        return jsonify([])

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history_data = json.load(f)
            user_history = [entry for entry in history_data if entry["email"] == email]
            user_history.sort(key=lambda x: x["timestamp"], reverse=True)  # Latest first
            return jsonify(user_history)

    return jsonify([])

@app.route('/')
def index():
    return "Backend is live!"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
