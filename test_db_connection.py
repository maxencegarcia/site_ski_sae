from flask import Flask, g
from connexion_db import get_db
import os

app = Flask(__name__)

with app.app_context():
    print("Testing database connection...")
    try:
        db = get_db()
        print("Success: Connection object created.")
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        print("Success: Query executed.")
        print("HOST used:", os.environ.get("HOST"))
    except Exception as e:
        print(f"Error: {e}")
