"""
Module: train_model.py
Trains a Scikit-Learn DecisionTreeClassifier to predict student academic risk.
Evaluates model with Stratified Train/Test Split, calculates comprehensive metrics,
and persists both the trained model and evaluation metadata.

DISCLOSURE & EDUCATIONAL NOTICE:
This model is trained on a synthetic pedagogical dataset for demonstrating machine learning
concepts in a B.Tech academic mini-project. Synthetic data metrics do not validate real-world
clinical or academic risk assessment accuracy.
"""

import os
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "ml" / "dataset" / "students.csv"
MODELS_DIR = BASE_DIR / "ml" / "models"
MODEL_PATH = MODELS_DIR / "risk_model.pkl"
METADATA_PATH = MODELS_DIR / "model_metadata.json"

FEATURE_NAMES = [
    "attendance",
    "internal_marks",
    "assignment_marks",
    "previous_percentage",
    "study_hours",
    "failed_subjects"
]

TARGET_NAME = "risk_label"
CLASS_NAMES = ["Low Risk", "Medium Risk", "High Risk"]

def train_and_evaluate_model(dataset_path=DATASET_PATH, model_path=MODEL_PATH, metadata_path=METADATA_PATH):
    """
    Executes end-to-end ML training pipeline:
    1. Loads dataset
    2. Validates features and clean nulls
    3. Performs stratified split
    4. Fits DecisionTreeClassifier
    5. Computes multi-class metrics & confusion matrix
    6. Saves .pkl model and .json metadata
    """
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    if not Path(dataset_path).exists():
        raise FileNotFoundError(f"Dataset not found at {dataset_path}. Run generate_dataset.py first.")

    # 1. Load dataset
    df = pd.read_csv(dataset_path)

    # 2. Validation & data cleaning
    df = df.dropna(subset=FEATURE_NAMES + [TARGET_NAME])
    for col in FEATURE_NAMES:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna()

    X = df[FEATURE_NAMES]
    y = df[TARGET_NAME]

    # Verify all classes exist
    unique_classes = sorted(y.unique())
    for cls in CLASS_NAMES:
        if cls not in unique_classes:
            raise ValueError(f"Required target class '{cls}' not present in dataset.")

    # 3. Stratified Train-Test Split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # 4. Fit Decision Tree Classifier
    # Constraining max_depth=6 prevents excessive overfitting and produces interpretable decision rules
    clf = DecisionTreeClassifier(
        criterion="gini",
        max_depth=6,
        min_samples_split=8,
        min_samples_leaf=4,
        random_state=42
    )
    clf.fit(X_train, y_train)

    # 5. Evaluate on Test Set
    y_pred = clf.predict(X_test)

    acc = float(accuracy_score(y_test, y_pred))
    prec_macro = float(precision_score(y_test, y_pred, labels=CLASS_NAMES, average="macro", zero_division=0))
    rec_macro = float(recall_score(y_test, y_pred, labels=CLASS_NAMES, average="macro", zero_division=0))
    f1_macro = float(f1_score(y_test, y_pred, labels=CLASS_NAMES, average="macro", zero_division=0))

    prec_weighted = float(precision_score(y_test, y_pred, labels=CLASS_NAMES, average="weighted", zero_division=0))
    rec_weighted = float(recall_score(y_test, y_pred, labels=CLASS_NAMES, average="weighted", zero_division=0))
    f1_weighted = float(f1_score(y_test, y_pred, labels=CLASS_NAMES, average="weighted", zero_division=0))

    cm = confusion_matrix(y_test, y_pred, labels=CLASS_NAMES).tolist()
    report_dict = classification_report(y_test, y_pred, labels=CLASS_NAMES, output_dict=True, zero_division=0)

    # Feature importances
    feature_importances = {
        feat: round(float(imp), 4)
        for feat, imp in zip(FEATURE_NAMES, clf.feature_importances_)
    }

    # 6. Save model to disk
    joblib.dump(clf, model_path)

    # 7. Save metadata and evaluation metrics to JSON
    metadata = {
        "model_type": "DecisionTreeClassifier",
        "parameters": {
            "criterion": "gini",
            "max_depth": 6,
            "min_samples_split": 8,
            "min_samples_leaf": 4,
            "random_state": 42
        },
        "feature_names": FEATURE_NAMES,
        "class_names": CLASS_NAMES,
        "dataset_summary": {
            "total_records": len(df),
            "train_size": len(X_train),
            "test_size": len(X_test),
            "class_distribution": y.value_counts().to_dict()
        },
        "metrics": {
            "accuracy": round(acc, 4),
            "precision_macro": round(prec_macro, 4),
            "recall_macro": round(rec_macro, 4),
            "f1_macro": round(f1_macro, 4),
            "precision_weighted": round(prec_weighted, 4),
            "recall_weighted": round(rec_weighted, 4),
            "f1_weighted": round(f1_weighted, 4)
        },
        "confusion_matrix": {
            "labels": CLASS_NAMES,
            "matrix": cm
        },
        "classification_report": report_dict,
        "feature_importances": feature_importances,
        "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "disclaimer": "Academic mini-project demonstration on synthetic dataset. Not a validated institutional prediction system."
    }

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    print("Model training and evaluation completed successfully.")
    print(f"Accuracy: {acc * 100:.2f}% | Macro F1: {f1_macro:.4f}")
    print(f"Saved model to: {model_path}")
    print(f"Saved metadata to: {metadata_path}")

    return metadata

if __name__ == "__main__":
    train_and_evaluate_model()
