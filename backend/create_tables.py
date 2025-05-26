from app import app
from app import db  # or from app import db, if models are in app.py

with app.app_context():
    db.create_all()
    print("✅ Tables created successfully.")
