"""
Automated tests for Flask application routes, web UI endpoints, and error handling.
"""

import pytest
from app import create_app
from config import TestingConfig

@pytest.fixture
def client():
    app = create_app(TestingConfig)
    with app.test_client() as client:
        yield client

def test_dashboard_route(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Academic Performance & Risk Dashboard" in res.data

def test_students_list_route(client):
    res = client.get("/students")
    assert res.status_code == 200
    assert b"Student Directory" in res.data

def test_predict_page_route(client):
    # GET
    res = client.get("/predict")
    assert res.status_code == 200
    assert b"AI-Based Student Academic Risk Predictor" in res.data

    # POST
    payload = {
        "student_name": "Test Web Candidate",
        "attendance": "82.0",
        "internal_marks": "74.0",
        "assignment_marks": "78.0",
        "previous_percentage": "75.0",
        "study_hours": "4.0",
        "failed_subjects": "0"
    }
    post_res = client.post("/predict", data=payload)
    assert post_res.status_code == 200
    assert b"Diagnostic Result" in post_res.data

def test_dsa_demo_route(client):
    res = client.get("/dsa-demo")
    assert res.status_code == 200
    assert b"Verification Console" in res.data

def test_model_evaluation_route(client):
    res = client.get("/model-evaluation")
    assert res.status_code == 200
    assert b"Decision Tree Model Evaluation" in res.data

def test_about_route(client):
    res = client.get("/about")
    assert res.status_code == 200
    assert b"About the System & Architectural Specification" in res.data

def test_api_predict_endpoint(client):
    payload = {
        "attendance": 85.0,
        "internal_marks": 75.0,
        "assignment_marks": 78.0,
        "previous_percentage": 80.0,
        "study_hours": 3.5,
        "failed_subjects": 0
    }
    res = client.post("/api/predict", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert "predicted_risk" in data
    assert "confidence_score" in data
    assert "recommendations" in data

def test_404_not_found_route(client):
    res = client.get("/non-existent-page-url-xyz")
    assert res.status_code == 404
    assert b"404" in res.data
