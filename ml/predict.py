"""
Module: predict.py
Handles loading the trained DecisionTreeClassifier model and producing risk predictions
with class probabilities and feature contribution insights.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
import joblib
from config import Config

FEATURE_NAMES = [
    "attendance",
    "internal_marks",
    "assignment_marks",
    "previous_percentage",
    "study_hours",
    "failed_subjects"
]

class RiskPredictor:
    """Predictor class encapsulating the loaded Scikit-Learn decision tree model."""

    def __init__(self, model_path: Optional[str] = None, metadata_path: Optional[str] = None):
        self.model_path = Path(model_path or Config.MODEL_PATH)
        self.metadata_path = Path(metadata_path or Config.METADATA_PATH)
        self.model = None
        self.metadata = None
        self._load_artifacts()

    def _load_artifacts(self) -> None:
        """Loads model and metadata files safely."""
        if self.model_path.exists():
            try:
                self.model = joblib.load(self.model_path)
            except Exception as e:
                print(f"Error loading model from {self.model_path}: {e}")
                self.model = None
        
        if self.metadata_path.exists():
            try:
                with open(self.metadata_path, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
            except Exception as e:
                print(f"Error reading metadata from {self.metadata_path}: {e}")
                self.metadata = None

    def is_model_ready(self) -> bool:
        """Checks if the trained model is loaded and ready for predictions."""
        return self.model is not None

    def predict(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes ML prediction on student input features.
        Returns:
            - predicted_risk: 'Low Risk' | 'Medium Risk' | 'High Risk'
            - probabilities: dict of class name -> probability
            - confidence_score: float probability of chosen class
            - indicators: list of key contributing factors
        """
        if not self.is_model_ready():
            self._load_artifacts()
            if not self.is_model_ready():
                raise RuntimeError("ML model is not available. Please train the model before predicting.")

        # Extract features in exact order
        try:
            features = [
                float(student_data.get("attendance", 0.0)),
                float(student_data.get("internal_marks", 0.0)),
                float(student_data.get("assignment_marks", 0.0)),
                float(student_data.get("previous_percentage", 0.0)),
                float(student_data.get("study_hours", 0.0)),
                int(student_data.get("failed_subjects", 0))
            ]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid input feature value: {e}")

        # Create 1-row DataFrame with named columns for scikit-learn
        df_row = pd.DataFrame([features], columns=FEATURE_NAMES)

        # Scikit-learn prediction
        prediction_label = self.model.predict(df_row)[0]
        
        # Class probabilities
        probabilities = {}
        confidence = 1.0
        if hasattr(self.model, "predict_proba"):
            proba_arr = self.model.predict_proba(df_row)[0]
            classes = self.model.classes_
            for cls_name, prob in zip(classes, proba_arr):
                probabilities[cls_name] = round(float(prob), 4)
            confidence = probabilities.get(prediction_label, 1.0)

        # Identify key contributing indicators
        indicators = []
        if features[0] < 75.0:
            indicators.append(f"Attendance is below academic target ({features[0]:.1f}%)")
        if features[1] < 45.0:
            indicators.append(f"Internal assessment marks require reinforcement ({features[1]:.1f}/100)")
        if features[2] < 50.0:
            indicators.append(f"Assignment completion marks are low ({features[2]:.1f}/100)")
        if features[4] < 2.5:
            indicators.append(f"Average self-study hours per day is low ({features[4]:.1f} hrs/day)")
        if features[5] > 0:
            indicators.append(f"Has {int(features[5])} subject backlog(s) needing remedial clearance")

        return {
            "predicted_risk": prediction_label,
            "confidence_score": round(confidence, 4),
            "probabilities": probabilities,
            "contributing_indicators": indicators,
            "features": dict(zip(FEATURE_NAMES, features))
        }

# Global singleton predictor instance
predictor = RiskPredictor()
