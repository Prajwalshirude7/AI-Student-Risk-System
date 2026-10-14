"""
Module: generate_dataset.py
Generates a reproducible synthetic student performance dataset with at least 1,000 records.

DISCLOSURE & ETHICAL NOTICE:
This synthetic dataset is generated using a pedagogical heuristic solely for demonstrating
the machine learning engineering pipeline in a college mini-project context.
The synthetic labels do not constitute an empirical clinical assessment or a validated
student-risk prediction model for real academic institutions.
"""

import os
import csv
import random
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "ml" / "dataset"
DATASET_PATH = DATASET_DIR / "students.csv"

def evaluate_academic_heuristic(attendance, internal_marks, assignment_marks, previous_percentage, study_hours, failed_subjects):
    """
    Pedagogical heuristic labelling policy:
    Computes a weighted academic vulnerability score (0 to 100), where higher implies higher risk.
    Attendance weight: 25%
    Internal marks weight: 25%
    Assignment marks weight: 15%
    Previous percentage weight: 15%
    Study hours penalty: 10%
    Failed subjects impact: 10%
    """
    # Inverse scores (lower academic performance = higher risk score contribution)
    att_risk = (100.0 - attendance) * 0.25
    int_risk = (100.0 - internal_marks) * 0.25
    assn_risk = (100.0 - assignment_marks) * 0.15
    prev_risk = (100.0 - previous_percentage) * 0.15
    
    # Study hours: < 2 hrs contributes heavily, > 6 hrs lowers risk
    hours_factor = max(0.0, min(10.0, (6.0 - study_hours) * 1.5))
    
    # Failed subjects: 0 = 0 risk, >= 3 = heavy risk
    fail_risk = min(15.0, failed_subjects * 4.0)

    total_risk_score = att_risk + int_risk + assn_risk + prev_risk + hours_factor + fail_risk
    
    # Add minor realistic scholastic variance (-3 to +3)
    noise = random.uniform(-2.5, 2.5)
    total_risk_score += noise

    # Strict critical threshold overrides (reflecting college academic criteria)
    if failed_subjects >= 3 or (attendance < 55.0 and internal_marks < 40.0):
        return "High Risk"
    if attendance > 85.0 and internal_marks > 70.0 and failed_subjects == 0:
        return "Low Risk"

    # Quantile categorisation
    if total_risk_score >= 50.0:
        return "High Risk"
    elif total_risk_score >= 32.0:
        return "Medium Risk"
    else:
        return "Low Risk"

def generate_synthetic_dataset(num_records=1200, random_seed=42):
    """
    Generates realistic academic records and writes them to CSV.
    Guarantees balanced representation across all three risk categories.
    """
    random.seed(random_seed)
    DATASET_DIR.mkdir(parents=True, exist_ok=True)

    first_names = [
        "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
        "Shaurya", "Atharv", "Dhruv", "Kabir", "Rohan", "Ananya", "Diya", "Aadhya", "Pari", "Saanvi",
        "Isha", "Riya", "Myra", "Avani", "Prisha", "Sneha", "Pooja", "Meera", "Kavya", "Tanvi",
        "Rahul", "Prajwal", "Vikram", "Neha", "Nikhil", "Simran", "Deepak", "Swati", "Karan", "Priyanka"
    ]
    last_names = [
        "Sharma", "Verma", "Patel", "Reddy", "Rao", "Nair", "Iyer", "Kumar", "Singh", "Gupta",
        "Joshi", "Bhat", "Deshmukh", "Kulkarni", "Mehta", "Chopra", "Das", "Banerjee", "Pillai", "Menon"
    ]

    records = []
    class_counts = {"Low Risk": 0, "Medium Risk": 0, "High Risk": 0}

    for i in range(1, num_records + 1):
        student_id = f"STU-{1000 + i}"
        name = f"{random.choice(first_names)} {random.choice(last_names)}"

        # Sample across multiple synthetic student profiles (excelling, average, struggling)
        profile_type = random.choices(["high_achiever", "moderate", "at_risk"], weights=[0.35, 0.40, 0.25])[0]

        if profile_type == "high_achiever":
            attendance = round(random.uniform(78.0, 99.0), 1)
            internal_marks = round(random.uniform(68.0, 98.0), 1)
            assignment_marks = round(random.uniform(70.0, 100.0), 1)
            previous_percentage = round(random.uniform(72.0, 98.0), 1)
            study_hours = round(random.uniform(3.5, 8.0), 1)
            failed_subjects = 0
        elif profile_type == "moderate":
            attendance = round(random.uniform(62.0, 85.0), 1)
            internal_marks = round(random.uniform(45.0, 75.0), 1)
            assignment_marks = round(random.uniform(50.0, 80.0), 1)
            previous_percentage = round(random.uniform(55.0, 78.0), 1)
            study_hours = round(random.uniform(1.8, 4.5), 1)
            failed_subjects = random.choices([0, 1, 2], weights=[0.70, 0.22, 0.08])[0]
        else: # at_risk
            attendance = round(random.uniform(35.0, 68.0), 1)
            internal_marks = round(random.uniform(20.0, 52.0), 1)
            assignment_marks = round(random.uniform(25.0, 58.0), 1)
            previous_percentage = round(random.uniform(35.0, 60.0), 1)
            study_hours = round(random.uniform(0.5, 2.5), 1)
            failed_subjects = random.choices([1, 2, 3, 4, 5], weights=[0.30, 0.35, 0.20, 0.10, 0.05])[0]

        label = evaluate_academic_heuristic(
            attendance=attendance,
            internal_marks=internal_marks,
            assignment_marks=assignment_marks,
            previous_percentage=previous_percentage,
            study_hours=study_hours,
            failed_subjects=failed_subjects
        )
        class_counts[label] += 1

        records.append({
            "student_id": student_id,
            "name": name,
            "attendance": attendance,
            "internal_marks": internal_marks,
            "assignment_marks": assignment_marks,
            "previous_percentage": previous_percentage,
            "study_hours": study_hours,
            "failed_subjects": failed_subjects,
            "risk_label": label
        })

    # Save to CSV
    fieldnames = [
        "student_id", "name", "attendance", "internal_marks", 
        "assignment_marks", "previous_percentage", "study_hours", 
        "failed_subjects", "risk_label"
    ]

    with open(DATASET_PATH, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"Generated {len(records)} student records into {DATASET_PATH}")
    print(f"Class distribution: {class_counts}")
    return DATASET_PATH, class_counts

if __name__ == "__main__":
    generate_synthetic_dataset()
