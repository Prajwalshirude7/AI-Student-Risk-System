"""
Automated tests for backend payload validation and academic metric bounds.
"""

import pytest
from services.student_service import StudentService

def test_valid_student_payload():
    valid_data = {
        "name": "Kavya Bhat",
        "attendance": 84.5,
        "internal_marks": 72.0,
        "assignment_marks": 76.5,
        "previous_percentage": 80.0,
        "study_hours": 3.5,
        "failed_subjects": 0
    }
    is_valid, err, cleaned = StudentService.validate_student_payload(valid_data)
    assert is_valid is True
    assert err is None
    assert cleaned["name"] == "Kavya Bhat"
    assert cleaned["attendance"] == 84.5

def test_empty_or_short_name():
    data = {
        "name": " ",
        "attendance": 75.0,
        "internal_marks": 60.0,
        "assignment_marks": 60.0,
        "previous_percentage": 60.0,
        "study_hours": 3.0,
        "failed_subjects": 0
    }
    is_valid, err, _ = StudentService.validate_student_payload(data)
    assert is_valid is False
    assert "name" in err.lower()

def test_attendance_bounds():
    # Negative attendance
    is_valid, err, _ = StudentService.validate_student_payload({
        "name": "Ananya", "attendance": -5.0, "internal_marks": 60.0,
        "assignment_marks": 60.0, "previous_percentage": 60.0,
        "study_hours": 3.0, "failed_subjects": 0
    })
    assert is_valid is False
    assert "attendance" in err.lower()

    # Attendance > 100
    is_valid, err, _ = StudentService.validate_student_payload({
        "name": "Ananya", "attendance": 105.0, "internal_marks": 60.0,
        "assignment_marks": 60.0, "previous_percentage": 60.0,
        "study_hours": 3.0, "failed_subjects": 0
    })
    assert is_valid is False
    assert "attendance" in err.lower()

def test_study_hours_bounds():
    # Study hours > 24 in a single day
    is_valid, err, _ = StudentService.validate_student_payload({
        "name": "Rohit", "attendance": 75.0, "internal_marks": 60.0,
        "assignment_marks": 60.0, "previous_percentage": 60.0,
        "study_hours": 26.0, "failed_subjects": 0
    })
    assert is_valid is False
    assert "study hours" in err.lower()

def test_negative_failed_subjects():
    is_valid, err, _ = StudentService.validate_student_payload({
        "name": "Rohit", "attendance": 75.0, "internal_marks": 60.0,
        "assignment_marks": 60.0, "previous_percentage": 60.0,
        "study_hours": 3.0, "failed_subjects": -2
    })
    assert is_valid is False
    assert "failed subjects" in err.lower()
