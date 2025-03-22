import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Flask-Konfiguration
class Config:
    SECRET_KEY = "supersecretkey"
    DEBUG = True
    DATA_FOLDER = os.path.join(BASE_DIR, "data")  # Nutzt den `data/` Ordner
