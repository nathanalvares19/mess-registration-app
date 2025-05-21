from flask import Flask, request, jsonify, session
from flask_cors import CORS
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
CORS(app)

# users database
USERS_FILE = 'users.json'

# Load users from file at startup
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
else:
    users = {}


# # Simple users dict with email: password in plain text (for testing only)
# users = {
#     'student@iith.ac.in': 'mypassword123'
# }

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

    user_email = session['user']

    registrations[user_email] = {
        'mess': mess,
        'plan': plan
    }

    print(f"Registered {user_email} for mess {mess} with plan {plan}")

    return jsonify({'message': 'Mess registration successful'})


if __name__ == '__main__':
    app.run(debug=True)
