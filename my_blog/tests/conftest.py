# tests/conftest.py
import os
import sys

def pytest_sessionstart(session):
    """Автоматически добавляем путь к проекту."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)