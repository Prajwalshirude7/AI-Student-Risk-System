"""Services package initialization."""
from .student_service import StudentService
from .prediction_service import PredictionService
from .recommendation_service import AcademicRecommendationService

__all__ = [
    "StudentService",
    "PredictionService",
    "AcademicRecommendationService"
]
