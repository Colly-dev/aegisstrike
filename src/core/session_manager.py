"""
AegisStrike - Session Manager
Persists scan results to local SQLite database and manages history.
"""

import sqlite3
import json
import time
from typing import Optional

DB_PATH = "databases/scans.db"

class SessionManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                mode TEXT,
                started_at REAL,
                ended_at REAL,
                results TEXT
            )
        """)
        conn.commit()
        conn.close()

    def save_scan(self, target: str, mode: str, results: dict) -> int:
        """Save a scan session to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO scans (target, mode, started_at, results) VALUES (?, ?, ?, ?)",
            (target, mode, time.time(), json.dumps(results))
        )
        scan_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return scan_id

    def get_history(self) -> list:
        """Retrieve scan history."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, target, mode, started_at FROM scans ORDER BY started_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [{"id": r[0], "target": r[1], "mode": r[2], "started_at": r[3]} for r in rows]
