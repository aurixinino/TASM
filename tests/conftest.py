"""
Test configuration and fixtures

This module contains pytest configuration and shared fixtures.
"""

import pytest
from pathlib import Path
import tempfile
import shutil

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        'numbers': [1, 2, 3, 4, 5],
        'strings': ['a', 'b', 'c'],
        'mixed': [1, 'two', 3.0, True]
    }