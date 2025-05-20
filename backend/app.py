from flask import Flask, request, jsonify, session
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
CORS(app)

# Simple users dict with email: password in plain text (for testing only)
users = {
    'student@iith.ac.in': 'mypassword123'
}

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
