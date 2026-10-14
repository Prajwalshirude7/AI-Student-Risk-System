"""
Module: recommendation_service.py
Generates actionable, non-judgmental, constructive academic recommendations
derived from student scholastic indicators.
"""

from typing import Dict, Any, List

class AcademicRecommendationService:
    """
    Generates tailored, respectful, and empowering educational guidance for students and mentors.
    """

    @staticmethod
    def generate_recommendations(features: Dict[str, Any], risk_level: str) -> List[str]:
        """
        Evaluates student attributes to formulate targeted recommendations.
        """
        recs = []
        attendance = float(features.get("attendance", 0.0))
        internal_marks = float(features.get("internal_marks", 0.0))
        assignment_marks = float(features.get("assignment_marks", 0.0))
        study_hours = float(features.get("study_hours", 0.0))
        failed_subjects = int(features.get("failed_subjects", 0))

        # Attendance guidance
        if attendance < 65.0:
            recs.append("Prioritize attending upcoming theory and laboratory sessions to satisfy institutional minimum attendance requirements.")
        elif attendance < 75.0:
            recs.append("Aim for consistent attendance across all subjects to maintain buffer margin above the 75% threshold.")

        # Internal marks guidance
        if internal_marks < 40.0:
            recs.append("Schedule one-on-one doubt clearing sessions with faculty mentors for core subjects scoring below passing criteria.")
            recs.append("Participate in peer study circles or department remedial coaching classes.")
        elif internal_marks < 60.0:
            recs.append("Review mid-term examination answer scripts to identify and practice challenging problem types.")

        # Assignment guidance
        if assignment_marks < 50.0:
            recs.append("Complete and submit upcoming assignments before deadlines to secure continuous evaluation credits.")

        # Study hours guidance
        if study_hours < 2.0:
            recs.append("Establish a daily structured revision schedule allocating at least 2.5 to 3 focused hours for core coursework.")
        elif study_hours < 3.5:
            recs.append("Maintain consistent daily study routines incorporating active recall and past university question papers.")

        # Backlog guidance
        if failed_subjects > 0:
            recs.append(f"Formulate a targeted semester backlog clearance plan for the {failed_subjects} pending course(s) with academic counselor.")

        # Risk-specific general advice
        if risk_level == "High Risk" and len(recs) == 0:
            recs.append("Consult department academic coordinator for personalized curriculum pacing and mentorship.")
        elif risk_level == "Low Risk":
            recs.append("Maintain existing positive academic habits and consider participating in competitive technical projects or seminar presentations.")

        return recs
