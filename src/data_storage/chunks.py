import sqlite3
from pathlib import Path

db_path = Path("data/user_data/time_storage.db")

def add_time_chunk(user_id, source_file, start_sec, end_sec, content):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO time_chunks (user_id, source, start_time, end_time, text)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, source_file, start_sec, end_sec, content))
        conn.commit()


def get_chunks_around_timestamp(user_id, source,  center, window):
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
            AND source = ?
            AND end_time >= ?
            AND start_time <= ?
            ORDER BY start_time ASC
        """, (user_id, source, start_time, end_time))

        rows = c.fetchall()
        return rows

def get_all_chunks_for_source(user_id, source_file):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT start_time, end_time, text FROM time_chunks
            WHERE user_id = ?
            AND source = ?
            ORDER BY start_time ASC
        """, (user_id, source_file))

        return c.fetchall()
