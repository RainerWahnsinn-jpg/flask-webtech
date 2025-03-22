from flask import Blueprint, render_template, request, redirect, url_for
import json
import os

studenten_bp = Blueprint("studenten", __name__)

# 📌 JSON-Handling
def load_studenten():
    if not os.path.exists("data/studenten.json"):
        with open("data/studenten.json", "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)
    with open("data/studenten.json", "r", encoding="utf-8") as file:
        return json.load(file)

def save_studenten(studenten):
    with open("data/studenten.json", "w", encoding="utf-8") as file:
        json.dump(studenten, file, indent=4)

# 🎓 Studentenübersicht
@studenten_bp.route('/')
def studenten():
    studenten_liste = load_studenten()
    return render_template('studenten.html', studenten=studenten_liste)

# 🆕 Studenten hinzufügen
@studenten_bp.route('/add', methods=['POST'])
def add_student():
    studenten_liste = load_studenten()
    new_id = max([s["id"] for s in studenten_liste], default=0) + 1
    new_student = {
        "id": new_id,
        "name": request.form["name"],
        "semester": int(request.form["semester"])
    }
    studenten_liste.append(new_student)
    save_studenten(studenten_liste)
    return redirect(url_for('studenten.studenten'))

# ❌ Studenten löschen (FEHLT VIELLEICHT!)
@studenten_bp.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    studenten_liste = load_studenten()
    studenten_liste = [s for s in studenten_liste if s["id"] != student_id]
    save_studenten(studenten_liste)
    return redirect(url_for('studenten.studenten'))
