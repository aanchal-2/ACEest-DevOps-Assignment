import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(
    os.environ.get("ACEEST_DB_PATH", str(BASE_DIR / "instance" / "aceest.db"))
)
def get_connection(db_path=None):
    path = Path(db_path or DB_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
def init_db(db_path=None):
    with get_connection(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL COLLATE NOCASE UNIQUE,
                membership_status TEXT NOT NULL DEFAULT 'Active'
                    CHECK (membership_status IN ('Active', 'Inactive'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                workout_type TEXT NOT NULL,
                duration_min INTEGER NOT NULL CHECK (duration_min > 0),
                FOREIGN KEY (client_id) REFERENCES clients(id)
                    ON DELETE CASCADE
            )
        """)
def add_client(name, db_path=None):
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO clients (name) VALUES (?)", (name.strip(),)
        )
        return cursor.lastrowid
def list_clients(db_path=None):
    with get_connection(db_path) as conn:
        rows = conn.execute(
            "SELECT id, name, membership_status FROM clients ORDER BY id"
        ).fetchall()
        return [dict(row) for row in rows]
def update_membership(client_id, status, db_path=None):
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            "UPDATE clients SET membership_status = ? WHERE id = ?",
            (status, client_id)
        )
        return cursor.rowcount > 0
def add_workout(client_id, workout_type, duration, db_path=None):
    with get_connection(db_path) as conn:
        client = conn.execute(
            "SELECT id FROM clients WHERE id = ?", (client_id,)
        ).fetchone()
        if client is None:
            return None
        cursor = conn.execute(
            """INSERT INTO workouts (client_id, workout_type, duration_min)
               VALUES (?, ?, ?)""",
            (client_id, workout_type.strip(), duration)
        )
        return cursor.lastrowid
def list_workouts(db_path=None):
    with get_connection(db_path) as conn:
        rows = conn.execute("""
            SELECT w.id, w.client_id, c.name AS client_name,
                   w.workout_type, w.duration_min
            FROM workouts w
            JOIN clients c ON c.id = w.client_id
            ORDER BY w.id
        """).fetchall()
        return [dict(row) for row in rows]
