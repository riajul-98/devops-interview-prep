"""
Configuration and constants
"""
from pathlib import Path

# Application info
APP_NAME = "DevOps Interview Prep"
VERSION = "1.1.0"

# File paths - Use absolute path for container
DEFAULT_QUESTIONS_FILE = "/app/data/questions/interview_questions.json"
PROGRESS_DIR = Path.home() / ".devops-ip"
PROGRESS_FILE = PROGRESS_DIR / "progress.json"

# Progress tracking settings
MIN_ATTEMPTS_FOR_WEAK_AREAS = 3
MAX_WEAK_AREAS_SHOWN = 5
DEFAULT_REVIEW_COUNT = 10

# Performance thresholds
EXCELLENT_THRESHOLD = 90
GOOD_THRESHOLD = 75
FAIR_THRESHOLD = 60

# UI Settings
SEPARATOR_LENGTH = 70
SUMMARY_SEPARATOR_LENGTH = 50
