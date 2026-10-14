"""
Automated tests for SQLite database initialization, constraints, and queries.
"""

import os
import gc
import tempfile
import sqlite3
import pytest
from database.db import init_db, reset_db, get_db_connection, execute_query, execute_mutation

@pytest.fixture
def temp_db():
    """Provides an isolated temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    init_db(path)
    yield path
    gc.collect()
    if os.path.exists(path):
        try:
            os.remove(path)
        except PermissionError:
            pass

def test_database_initialization(temp_db):
    """Verify tables are created properly with correct schema."""
    conn = get_db_connection(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row["name"] for row in cursor.fetchall()]
    conn.close()

    assert "students" in tables
    assert "predictions" in tables
    assert "operations_log" in tables

def test_student_insertion_and_query(temp_db):
    """Verify parameterized insertion and querying of student records."""
    query = """
    INSERT INTO students (
        student_id, name, attendance, internal_marks, assignment_marks,
        previous_percentage, study_hours, failed_subjects, predicted_risk,
        created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    params = ("STU-9999", "Test Student", 85.0, 75.0, 80.0, 78.0, 4.0, 0, "Low Risk", "2026-10-12", "2026-10-12")
    res = execute_mutation(query, params, db_path=temp_db)
    assert res["last_row_id"] is not None

    record = execute_query("SELECT * FROM students WHERE student_id = ?;", ("STU-9999",), db_path=temp_db, fetchone=True)
    assert record is not None
    assert record["name"] == "Test Student"
    assert record["attendance"] == 85.0

def test_database_check_constraints(temp_db):
    """Verify CHECK constraints enforce valid academic boundaries (e.g. attendance <= 100)."""
    invalid_query = """
    INSERT INTO students (
        student_id, name, attendance, internal_marks, assignment_marks,
        previous_percentage, study_hours, failed_subjects, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    # Attendance 150.0 violates attendance <= 100.0
    with pytest.raises(sqlite3.IntegrityError):
        execute_mutation(
            invalid_query,
            ("STU-ERR1", "Invalid Att", 150.0, 50.0, 50.0, 50.0, 2.0, 0, "2026-10-12", "2026-10-12"),
            db_path=temp_db
        )
