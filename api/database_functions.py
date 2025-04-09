"""Functions to communicate with the database."""

from datetime import datetime

from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection


def get_db_connection() -> connection:
    """Returns a live connection to the DB."""

    return connect(dbname="writing_app",
                   cursor_factory=RealDictCursor)


def load_all_entries(conn: connection) -> list[dict]:
    """Returns entries from the database."""

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM entry;")
        entries = cur.fetchall()
    
    return entries


def is_valid_entry(entry: dict) -> bool:
    """Returns if an entry is valid."""

    for k in ["body", "title", "author"]:
        if k not in entry or not entry[k]:
            return False
    return True


def save_new_entry(conn: connection, entry: dict) -> dict:
    """Saves an entry to the database."""

    q = """
    INSERT INTO entry
        (title, body, author_id)
    VALUES
        (%s, %s, %s)
    RETURNING *;
    """

    with conn.cursor() as cur:

        try:
            cur.execute("SELECT author_id FROM author WHERE author_name = %s;",
                        (entry["author"],))
            
            author_id = cur.fetchone()["author_id"]
        except:
            raise ValueError("Author not found.")

        cur.execute(q, (entry["title"],
                        entry["body"],
                        author_id))
        
        entry = cur.fetchone()

    return entry

if __name__ == "__main__":

    with get_db_connection() as conn:
        print(conn)
