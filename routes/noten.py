from flask import Blueprint, render_template, request, redirect, url_for
import json
import os
from config import Config

noten_bp = Blueprint("noten", __name__)

# 📌 Noten-Handling mit JSON-Datei
def load_noten():
    path = os.path.join(Config.DATA_FOLDER, "noten.json")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def save_noten(noten):
    path = os.path.join(Config.DATA_FOLDER, "noten.json")
    with open(path, "w", encoding="utf-8") as file:
        json.dump(noten, file, indent=4)

# 📖 Notenübersicht
@noten_bp.route('/')
def noten():
    noten_liste = load_noten()
    if not noten_liste:
        durchschnitt = 0
    else:
        durchschnitt = round(sum(float(n['note']) for n in noten_liste) / len(noten_liste), 2)

    return render_template('noten.html', noten=noten_liste, durchschnitt=durchschnitt)


# 🆕 Noten hinzufügen
@noten_bp.route('/add', methods=['POST'])
def add_note():
    noten_liste = load_noten()
    new_id = max([n["id"] for n in noten_liste], default=0) + 1
    new_note = {"id": new_id, "fach": request.form["fach"], "note": float(request.form["note"])}
    noten_liste.append(new_note)
    save_noten(noten_liste)
    return redirect(url_for('noten.noten'))
