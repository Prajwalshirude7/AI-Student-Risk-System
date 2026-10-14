"""
Automated tests for Student Service CRUD and undo operations.
"""

import os
import tempfile
import pytest
from database.db import init_db
from services.student_service import StudentService

@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    init_db(path)
    yield path
    if os.path.exists(path):
        os.remove(path)

def test_student_crud_lifecycle(temp_db):
    """Test full lifecycle: create, read, update, delete."""
    payload = {
        "student_id": "STU-8001",
        "name": "Vivaan Joshi",
        "attendance": 82.5,
        "internal_marks": 70.0,
        "assignment_marks": 75.0,
        "previous_percentage": 78.0,
        "study_hours": 4.0,
        "failed_subjects": 0
    }

    # 1. Create
    created = StudentService.create_student(payload, db_path=temp_db)
    assert created["student_id"] == "STU-8001"
    assert created["name"] == "Vivaan Joshi"

    # 2. Read
    fetched = StudentService.get_student_by_id("STU-8001", db_path=temp_db)
    assert fetched is not None
    assert fetched["attendance"] == 82.5

    # 3. Update
    updated_payload = dict(payload)
    updated_payload["attendance"] = 88.0
    updated = StudentService.update_student("STU-8001", updated_payload, db_path=temp_db)
    assert updated["attendance"] == 88.0

    # 4. Delete
    deleted = StudentService.delete_student("STU-8001", db_path=temp_db)
    assert deleted is True
    assert StudentService.get_student_by_id("STU-8001", db_path=temp_db) is None

def test_undo_student_deletion(temp_db):
    """Test LIFO stack undo restores a deleted student."""
    payload = {
        "student_id": "STU-8002",
        "name": "Diya Nair",
        "attendance": 65.0,
        "internal_marks": 50.0,
        "assignment_marks": 55.0,
        "previous_percentage": 60.0,
        "study_hours": 2.0,
        "failed_subjects": 1
    }
    StudentService.create_student(payload, db_path=temp_db)
    StudentService.delete_student("STU-8002", db_path=temp_db)
    assert StudentService.get_student_by_id("STU-8002", db_path=temp_db) is None

    # Trigger undo
    undo_res = StudentService.undo_last_operation(db_path=temp_db)
    assert undo_res["success"] is True

    restored = StudentService.get_student_by_id("STU-8002", db_path=temp_db)
    assert restored is not None
    assert restored["name"] == "Diya Nair"
