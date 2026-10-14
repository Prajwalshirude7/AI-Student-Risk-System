"""
Automated tests for ML prediction pipeline, model inference, and recommendation generation.
"""

import pytest
from ml.predict import RiskPredictor, predictor
from services.recommendation_service import AcademicRecommendationService

def test_model_inference_and_categories():
    """Verify inference returns valid categories and probability structures."""
    sample_student = {
        "attendance": 88.0,
        "internal_marks": 78.0,
        "assignment_marks": 82.0,
        "previous_percentage": 80.0,
        "study_hours": 4.5,
        "failed_subjects": 0
    }

    res = predictor.predict(sample_student)
    assert res["predicted_risk"] in ["Low Risk", "Medium Risk", "High Risk"]
    assert 0.0 <= res["confidence_score"] <= 1.0

    # Probabilities sum to approximately 1.0
    probs = res["probabilities"]
    assert len(probs) == 3
    prob_sum = sum(probs.values())
    assert abs(prob_sum - 1.0) < 0.05

def test_high_risk_inference():
    """Verify student with low attendance and marks is flagged at higher vulnerability."""
    struggling_student = {
        "attendance": 42.0,
        "internal_marks": 25.0,
        "assignment_marks": 30.0,
        "previous_percentage": 40.0,
        "study_hours": 0.8,
        "failed_subjects": 3
    }
    res = predictor.predict(struggling_student)
    assert res["predicted_risk"] in ["Medium Risk", "High Risk"]
    assert len(res["contributing_indicators"]) > 0

def test_academic_recommendations():
    """Verify non-judgmental recommendations are produced for struggling indicators."""
    features = {
        "attendance": 55.0,
        "internal_marks": 35.0,
        "assignment_marks": 40.0,
        "study_hours": 1.2,
        "failed_subjects": 2
    }
    recs = AcademicRecommendationService.generate_recommendations(features, "High Risk")
    assert len(recs) >= 2
    # Ensure constructive terminology
    assert any("attendance" in r.lower() for r in recs)
    assert any("backlog" in r.lower() or "revision" in r.lower() or "faculty" in r.lower() for r in recs)

def test_missing_model_handling():
    """Verify graceful handling when model path is non-existent."""
    dummy_predictor = RiskPredictor(model_path="non_existent_model.pkl", metadata_path="non_existent.json")
    with pytest.raises(RuntimeError):
        dummy_predictor.predict({
            "attendance": 80.0, "internal_marks": 70.0, "assignment_marks": 70.0,
            "previous_percentage": 70.0, "study_hours": 3.0, "failed_subjects": 0
        })
