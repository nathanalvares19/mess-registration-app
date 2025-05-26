# app.py  –  unified backend for Mess Registration
# -----------------------------------------------
from flask import Flask, request, jsonify, session
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo           # Python ≥ 3.9
from flask_cors import CORS
import json, os

# ─── App + session config ────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "your_secret_key_here"

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,
    PERMANENT_SESSION_LIFETIME=timedelta(days=7)
)

CORS(app)

# ─── File paths ───────────────────────────────────────────────────────
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
USERS_FILE      = os.path.join(BASE_DIR, "users.json")
MESS_DATA_FILE  = os.path.join(BASE_DIR, "mess_data.json")
HISTORY_FILE    = os.path.join(BASE_DIR, "history_data.json")

# ─── Load data into memory at startup ─────────────────────────────────
users = {}
if os.path.exists(USERS_FILE):
    with open(USERS_FILE) as f:
        users = json.load(f)

registrations = {}
if os.path.exists(MESS_DATA_FILE):
    with open(MESS_DATA_FILE) as f:
        registrations = json.load(f)

# ─── Helper for IST timestamp ─────────────────────────────────────────
def ist_now(fmt="%Y-%m-%dT%H:%M:%S"):
    return datetime.now(ZoneInfo("Asia/Kolkata")).strftime(fmt)

# ─── Auth endpoints ──────────────────────────────────────────────────
@app.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    email, password = data.get("email"), data.get("password")
    if email in users and users[email] == password:
        session["user"] = email
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid email or password"}), 401


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json or {}
    email, password = data.get("email"), data.get("password")
    if email in users:
        return jsonify({"message": "Account already exists"}), 409
    users[email] = password
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)
    return jsonify({"message": "Sign up successful"}), 200

# ─── Mess registration ───────────────────────────────────────────────
@app.route("/register-mess", methods=["POST"])
def register_mess():
    if "user" not in session:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json or {}
    mess, plan = data.get("mess"), data.get("plan")
    if not mess or not plan:
        return jsonify({"message": "Missing mess or plan selection"}), 400

    email = session["user"]
    ts    = ist_now()

    registrations[email] = {
        "mess":         mess,
        "plan":         plan,
        "registeredOn": ts
    }
    with open(MESS_DATA_FILE, "w") as f:
        json.dump(registrations, f, indent=2)

    # history
    hist_entry = {
        "email": email,
        "mess": mess,
        "plan": plan,
        "timestamp": ts,
        "status": "registered"
    }
    _append_history(hist_entry)

    return jsonify({"message": "Mess registration successful"}), 200

# ─── Helper to append to history file ─────────────────────────────────
def _append_history(entry: dict):
    hist = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            hist = json.load(f)
    hist.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(hist, f, indent=2)

# ─── Admin: list all registrations ────────────────────────────────────
@app.route("/api/registrations", methods=["GET"])
def list_registrations():
    if not os.path.exists(MESS_DATA_FILE):
        return jsonify([]), 200
    with open(MESS_DATA_FILE) as f:
        data = json.load(f)
    return jsonify([{**rec, "email": email} for email, rec in data.items()]), 200

# ─── Update (admin) a student’s mess/plan ─────────────────────────────
@app.route("/api/update-registration", methods=["POST"])
def update_registration():
    data = request.json or {}
    email, mess, plan = data.get("email"), data.get("mess"), data.get("plan")
    if not (email and mess and plan):
        return jsonify({"error": "Missing field"}), 400
    if email not in registrations:
        return jsonify({"error": "Email not found"}), 404

    registrations[email]["mess"] = mess
    registrations[email]["plan"] = plan
    registrations[email]["registeredOn"] = ist_now()

    with open(MESS_DATA_FILE, "w") as f:
        json.dump(registrations, f, indent=2)

    return jsonify({"message": "Updated"}), 200

# ─── Utilities for logged-in student ──────────────────────────────────
@app.route("/current-user")
def current_user():
    return jsonify({"email": session.get("user")}), 200 if "user" in session else 401


@app.route("/mess_data")
def get_mess_data():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    rec = registrations.get(session["user"])
    return jsonify(rec or {"error": "User not registered"}), 200 if rec else 404


@app.route("/unregister-user")
def unregister_user():
    email = session.get("user")
    if not email:
        return jsonify({"error": "Unauthorized"}), 401
    if email not in registrations:
        return jsonify({"error": "User not registered"}), 404

    del registrations[email]
    with open(MESS_DATA_FILE, "w") as f:
        json.dump(registrations, f, indent=2)

    _append_history({
        "email": email,
        "mess": "-",
        "plan": "-",
        "timestamp": ist_now(),
        "status": "unregistered"
    })
    return jsonify({"message": "User unregistered successfully"}), 200


@app.route("/get-history")
def get_history():
    email = session.get("user")
    if not email or not os.path.exists(HISTORY_FILE):
        return jsonify([])
    with open(HISTORY_FILE) as f:
        hist = json.load(f)
    user_hist = [h for h in hist if h["email"] == email]
    user_hist.sort(key=lambda x: x["timestamp"], reverse=True)
    return jsonify(user_hist), 200

# ─── Root ──────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return "Backend is live!"

# ─── Run ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run()