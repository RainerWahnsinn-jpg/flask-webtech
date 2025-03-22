from flask import Blueprint, render_template, request, redirect, url_for, session
import json
import os
from config import Config

auth_bp = Blueprint("auth", __name__)

# 📌 Nutzer-Handling mit JSON-Datei
def load_users():
    path = os.path.join(Config.DATA_FOLDER, "users.json")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump({}, file, indent=4)
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def save_users(users):
    path = os.path.join(Config.DATA_FOLDER, "users.json")
    with open(path, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)

# 🔐 Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    users = load_users()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message="Login fehlgeschlagen.")
    return render_template('login.html')

# 🚪 Logout
@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))

# 📝 Registrierung
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    users = load_users()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('register.html', message="Benutzer existiert bereits!")
        users[username] = password
        save_users(users)
        return redirect(url_for('auth.login'))
    return render_template('register.html')
