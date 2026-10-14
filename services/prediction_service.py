"""
Module: prediction_service.py
Coordinates ML inference, recommendations generation, database history persistence,
and FIFO batch processing using the custom PredictionQueue.
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from database.db import execute_query, execute_mutation
from ml.predict import predictor
from services.recommendation_service import AcademicRecommendationService
from dsa.queue import PredictionQueue

# Global FIFO Queue for asynchronous / batch prediction requests
prediction_queue = PredictionQueue()

class PredictionService:
    """Manages risk prediction workflows, FIFO queue dispatching, and audit logging."""

    @classmethod
    def predict_and_record(
        cls,
        student_data: Dict[str, Any],
        student_id: Optional[str] = None,
        student_name: Optional[str] = None,
        save_to_db: bool = True,
        db_path=None
    ) -> Dict[str, Any]:
        """
        Runs ML prediction, attaches recommendations, and optionally saves to SQLite.
        """
        # Execute Scikit-Learn Decision Tree prediction
        ml_result = predictor.predict(student_data)
        predicted_risk = ml_result["predicted_risk"]
        confidence = ml_result["confidence_score"]
        probabilities = ml_result["probabilities"]
        indicators = ml_result["contributing_indicators"]

        # Generate constructive educational recommendations
        recommendations = AcademicRecommendationService.generate_recommendations(
            features=student_data,
            risk_level=predicted_risk
        )

        record_id = None
        now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if save_to_db:
            # 1. Insert into predictions history table
            query = """
            INSERT INTO predictions (
                student_id, student_name, attendance, internal_marks,
                assignment_marks, previous_percentage, study_hours,
                failed_subjects, predicted_risk, confidence_score,
                probabilities_json, recommendations_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
            params = (
                student_id or "ANONYMOUS",
                student_name or student_data.get("name", "Anonymous Student"),
                float(student_data["attendance"]),
                float(student_data["internal_marks"]),
                float(student_data["assignment_marks"]),
                float(student_data["previous_percentage"]),
                float(student_data["study_hours"]),
                int(student_data["failed_subjects"]),
                predicted_risk,
                confidence,
                json.dumps(probabilities),
                json.dumps(recommendations),
                now_ts
            )
            res = execute_mutation(query, params, db_path=db_path)
            record_id = res["last_row_id"]

            # 2. If student_id corresponds to an existing enrolled student, update their profile
            if student_id:
                execute_mutation(
                    """
                    UPDATE students SET
                        predicted_risk = ?,
                        risk_probability = ?,
                        updated_at = ?
                    WHERE student_id = ?;
                    """,
                    (predicted_risk, confidence, now_ts, student_id),
                    db_path=db_path
                )

        return {
            "prediction_id": record_id,
            "student_id": student_id,
            "student_name": student_name or student_data.get("name", "Anonymous"),
            "predicted_risk": predicted_risk,
            "confidence_score": confidence,
            "probabilities": probabilities,
            "contributing_indicators": indicators,
            "recommendations": recommendations,
            "features": student_data,
            "created_at": now_ts
        }

    @classmethod
    def enqueue_prediction(cls, payload: Dict[str, Any]) -> int:
        """
        Pushes a prediction request to the FIFO queue.
        Returns the new queue size.
        """
        prediction_queue.enqueue(payload)
        return prediction_queue.size()

    @classmethod
    def process_queue_synchronously(cls, db_path=None) -> List[Dict[str, Any]]:
        """
        Processes all queued prediction requests in FIFO sequence.
        Demonstrates practical application of the Queue data structure.
        """
        results = []
        while not prediction_queue.is_empty():
            task = prediction_queue.dequeue()
            if task:
                result = cls.predict_and_record(
                    student_data=task["data"],
                    student_id=task.get("student_id"),
                    student_name=task.get("student_name"),
                    save_to_db=task.get("save_to_db", True),
                    db_path=db_path
                )
                results.append(result)
        return results

    @classmethod
    def get_prediction_history(cls, limit: int = 50, db_path=None) -> List[Dict[str, Any]]:
        """Retrieves past prediction audit log from SQLite."""
        rows = execute_query(
            "SELECT * FROM predictions ORDER BY id DESC LIMIT ?;",
            (limit,),
            db_path=db_path
        )
        history = []
        for r in rows:
            item = dict(r)
            if item.get("probabilities_json"):
                try:
                    item["probabilities"] = json.loads(item["probabilities_json"])
                except Exception:
                    item["probabilities"] = {}
            if item.get("recommendations_json"):
                try:
                    item["recommendations"] = json.loads(item["recommendations_json"])
                except Exception:
                    item["recommendations"] = []
            history.append(item)
        return history
