import sqlite3
from pathlib import Path

db_path = Path("data/user_data/documents.db")

def list_documents(user_id):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT uuid, name, type, summary, upload_time FROM documents WHERE user_id=? ORDER BY upload_time DESC",
            (user_id,)
        )
        return c.fetchall()

if __name__ == "__main__":
    print(list_documents("user1"))