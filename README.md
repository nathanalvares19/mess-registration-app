# 🍽️ Mess Registration App

A full-stack web application built for college students to register/unregister for mess plans on a weekly or monthly basis. Designed with separate dashboards for students and admins, this app makes it easy to manage mess operations, monitor registrations, and communicate announcements — all from a clean and responsive interface.

---

## 📌 Features

### 👤 Student Dashboard

- Register and log in
- Choose mess plans (weekly or monthly)
- View current registration status
- Track historical registrations

### 🛠️ Admin Dashboard

- View all student registrations
- Download CSV reports
- Broadcast announcements to students
- Manage mess plan options (extendable)

### 🧠 Tech Stack

| Part     | Tech Used                                         |
| -------- | ------------------------------------------------- |
| Frontend | HTML, CSS, Vanilla JS                             |
| Backend  | Python + Flask                                    |
| Database | SQLite (can be extended to MongoDB)               |
| Auth     | Basic session/auth logic (can be extended to JWT) |
| Hosting  | Netlify (frontend) + Render (backend)             |

---

## 🚀 Getting Started

### ⚙️ Backend Setup (Flask)

1. Navigate to the backend folder:

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python run.py
   ```

### 🌐 Frontend

- Simply open `frontend/login.html` or deploy using Netlify/GitHub Pages.
- Connect it to the backend by updating `fetch()` URLs.

---
