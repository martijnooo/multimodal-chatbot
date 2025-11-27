import sqlite3
from pathlib import Path

db_path = Path("data/user_data/documents.db")

def add_document(user_id, name, type_, summary):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO documents (user_id, name, type, summary) VALUES (?, ?, ?, ?)",
            (user_id, name, type_, summary)
        )
        conn.commit()