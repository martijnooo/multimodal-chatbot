import sqlite3
from pathlib import Path

db_path = Path("data/user_data/time_storage.db")

def add_time_chunk(user_id, document_uuid, start_sec, end_sec, content):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO time_chunks (user_id, document_uuid, start_time, end_time, text)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, document_uuid, start_sec, end_sec, content))
        conn.commit()


def get_chunks_around_timestamp(user_id, document_uuid,  center, window):
    """
    Returns all chunks whose [start, end] interval intersects 
    with (timestamp - window, timestamp + window)
    """
    start_time = center - window
    end_time = center + window
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT start_time, end_time, text FROM time_chunks
            WHERE user_id = ?
            AND document_uuid  = ?
            AND end_time >= ?
            AND start_time <= ?
            ORDER BY start_time ASC
        """, (user_id, document_uuid, start_time, end_time))

        rows = c.fetchall()
        return rows
    
# ---------------------------
# Page-based chunks
# ---------------------------
def add_page_chunk(user_id, document_uuid, page, content):
    """
    Stores page-based chunks (for PDF/DOCX) in the same database.
    """
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO time_chunks (user_id, document_uuid, page, text)
            VALUES (?, ?, ?, ?)
        """, (user_id, document_uuid, page, content))
        conn.commit()


def get_chunks_around_page(user_id, document_uuid, page):
    """
    Retrieve chunks on a certain page
    """

    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT page, text FROM time_chunks
            WHERE user_id = ?
            AND document_uuid = ?
            AND page = ?
            ORDER BY page ASC
        """, (user_id, document_uuid, page))
        return c.fetchall()

def get_all_chunks_for_source(user_id, document_uuid):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT text FROM time_chunks
            WHERE user_id = ?
            AND document_uuid  = ?
        """, (user_id, document_uuid))

        return c.fetchall()
    

if __name__ == "__main__":
    print(get_chunks_around_page("user1","663b19a2-1e79-43f7-898e-f19c836c08dc", 2))
