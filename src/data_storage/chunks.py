import sqlite3
from pathlib import Path

db_path = Path("data/user_data/time_storage.db")

def add_time_chunk(user_id, source, start, end, text):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
        INSERT INTO time_chunks (user_id, source, start, end, text)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, source, start, end, text))
        conn.commit()

def get_chunks_around_timestamp(user_id, source, start_time, end_time):
    """
    Returns all chunks whose [start, end] interval intersects 
    with (timestamp - window, timestamp + window)
    """
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT start, end, text FROM time_chunks
            WHERE user_id = ?
            AND source = ?
            AND end => ?
            AND start <= ?
            ORDER BY start ASC
        """, (user_id, source, start_time, end_time))

        rows = c.fetchall()
        return rows

def get_all_chunks_for_source(user_id, source):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT start, end, text FROM time_chunks
            WHERE user_id = ? AND source = ?
            ORDER BY start ASC
        """, (user_id, source))

        rows = c.fetchall()
        return rows