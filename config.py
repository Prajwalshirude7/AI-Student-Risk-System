import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "academic-risk-system-secret-key-2026-btech")
    
    # Database Configuration
    DATABASE_PATH = os.environ.get("DATABASE_PATH", str(BASE_DIR / "database" / "students.db"))
    
    # Dataset and Model Paths
    DATASET_PATH = os.environ.get("DATASET_PATH", str(BASE_DIR / "ml" / "dataset" / "students.csv"))
    MODEL_PATH = os.environ.get("MODEL_PATH", str(BASE_DIR / "ml" / "models" / "risk_model.pkl"))
    METADATA_PATH = os.environ.get("METADATA_PATH", str(BASE_DIR / "ml" / "models" / "model_metadata.json"))
    
    # App Settings
    DEBUG = False
    TESTING = False
    HOST = "127.0.0.1"
    PORT = 5000


class TestingConfig(Config):
    """Configuration for automated test suite."""
    TESTING = True
    DEBUG = True
    DATABASE_PATH = str(BASE_DIR / "database" / "test_students.db")
