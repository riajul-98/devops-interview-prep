"""
Pytest configuration and fixtures
"""
import pytest
from pathlib import Path

@pytest.fixture
def sample_questions_file():
    """Provide path to sample questions file for testing"""
    return Path(__file__).parent / "fixtures" / "sample_questions.json"

@pytest.fixture
def temp_progress_dir(tmp_path):
    """Provide temporary directory for progress tracking tests"""
    return tmp_path / ".devops-ip-test"
