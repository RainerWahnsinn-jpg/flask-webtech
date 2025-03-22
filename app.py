from flask import Flask, render_template, redirect, url_for, request, session
from routes.auth import auth_bp
from routes.studenten import studenten_bp
from routes.noten import noten_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ✅ Blueprints registrieren
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(studenten_bp, url_prefix='/studenten')
app.register_blueprint(noten_bp, url_prefix='/noten')

# 🔐 Login-Seite (Vorgeschaltet)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "passwort":
            session["username"] = username
            return redirect(url_for("home"))
        return render_template("login.html", message="❌ Falsche Anmeldedaten")
    return render_template("login.html")

# 🚪 Logout
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

# 🏠 Startseite (Zugang nur wenn eingeloggt)
@app.route("/")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

# ❌ Fehlerseite (404)
@app.errorhandler(404)
def nicht_gefunden(error):
    return render_template("404.html"), 404

# 🏁 Flask starten
if __name__ == "__main__":
    app.run(debug=True)
