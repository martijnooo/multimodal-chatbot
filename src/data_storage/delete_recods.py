import sqlite3
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def delete_document(uuid: str):
    """Delete a document from the main document store by UUID."""
    DB_PATH = Path("data/user_data/documents.db")
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM documents WHERE uuid = ?", (uuid,))
        conn.commit()
        logger.info(f"Document with UUID {uuid} has been deleted from documents.db")
    except Exception as e:
        logger.error(f"Error deleting document {uuid}: {e}")
    finally:
        conn.close()
