import sqlite3
from typing import List, Dict, Tuple, Optional

DB_PATH = 'database.db'


def _get_conn():
    return sqlite3.connect(DB_PATH)


def get_last() -> Optional[Tuple[int, str]]:
    """Return the most recent row as (id, data) or None if empty."""
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, data FROM data ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return row


def insert_data(text: str) -> int:
    """Insert text into data table. Returns the inserted row id."""
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO data (data) VALUES (?)", (text,))
    conn.commit()
    rowid = cur.lastrowid
    conn.close()
    return rowid


def delete_data(rowid: int) -> bool:
    """Delete a row by id. Returns True if operation succeeded."""
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM data WHERE id = ?", (rowid,))
    conn.commit()
    conn.close()
    return True


def get_all_data() -> List[Dict[str, object]]:
    """Return all rows as list of dicts {'id': int, 'data': str}.

    This keeps the shape predictable for JSON serialization.
    """
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, data FROM data ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return [{'id': r[0], 'data': r[1]} for r in rows]


def clear_all() -> int:
    """Delete all rows from the data table. Returns the number of deleted rows."""
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM data")
    deleted = conn.total_changes
    conn.commit()
    conn.close()
    return deleted


