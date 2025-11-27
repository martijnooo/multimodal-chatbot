import sqlite3
from pathlib import Path

DB_PATH = Path("data/user_data/documents.db")

def clear_all_documents():
    """
    Deletes all records from the documents table.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM documents")  # remove all rows
    conn.commit()
    conn.close()
    return "All documents have been deleted."


if __name__ == "__main__":
    clear_all_documents()
