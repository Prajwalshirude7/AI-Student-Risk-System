import sqlite3
import os
from pathlib import Path
from config import Config

def get_db_path():
    """Return the database file path from config or environment."""
    db_path = Config.DATABASE_PATH
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    return db_path

def get_db_connection(db_path=None):
    """Establish and return an SQLite connection with Row factory."""
    if db_path is None:
        db_path = get_db_path()
    else:
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(db_path=None):
    """
    Initialize SQLite database tables if they do not already exist.
    Preserves existing records across application restarts.
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    # Students table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        attendance REAL NOT NULL CHECK (attendance >= 0.0 AND attendance <= 100.0),
        internal_marks REAL NOT NULL CHECK (internal_marks >= 0.0 AND internal_marks <= 100.0),
        assignment_marks REAL NOT NULL CHECK (assignment_marks >= 0.0 AND assignment_marks <= 100.0),
        previous_percentage REAL NOT NULL CHECK (previous_percentage >= 0.0 AND previous_percentage <= 100.0),
        study_hours REAL NOT NULL CHECK (study_hours >= 0.0 AND study_hours <= 24.0),
        failed_subjects INTEGER NOT NULL CHECK (failed_subjects >= 0),
        predicted_risk TEXT NOT NULL DEFAULT 'Not Predicted',
        risk_probability REAL DEFAULT 0.0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)

    # Predictions history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        student_name TEXT,
        attendance REAL NOT NULL,
        internal_marks REAL NOT NULL,
        assignment_marks REAL NOT NULL,
        previous_percentage REAL NOT NULL,
        study_hours REAL NOT NULL,
        failed_subjects INTEGER NOT NULL,
        predicted_risk TEXT NOT NULL,
        confidence_score REAL NOT NULL,
        probabilities_json TEXT,
        recommendations_json TEXT,
        created_at TEXT NOT NULL
    );
    """)

    # Operations log table (for Stack undo and audit demonstration)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS operations_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        operation_type TEXT NOT NULL,
        student_id TEXT NOT NULL,
        snapshot_data TEXT NOT NULL,
        timestamp TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()

def reset_db(db_path=None):
    """
    Reset database tables completely (for testing or explicit administrator reset).
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS operations_log;")
    cursor.execute("DROP TABLE IF EXISTS predictions;")
    cursor.execute("DROP TABLE IF EXISTS students;")
    conn.commit()
    conn.close()
    init_db(db_path)

def execute_query(query, params=(), db_path=None, fetchone=False):
    """Safely execute parameterized read query."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone() if fetchone else cursor.fetchall()
    conn.close()
    return result

def execute_mutation(query, params=(), db_path=None):
    """Safely execute parameterized write query (insert/update/delete)."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(query, params)
    last_row_id = cursor.lastrowid
    row_count = cursor.rowcount
    conn.commit()
    conn.close()
    return {"last_row_id": last_row_id, "row_count": row_count}
