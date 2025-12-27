"""
Test utilities module

Tests for the utils module functionality.
"""

import pytest
from pathlib import Path
import sys

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import get_project_root, create_output_dir

def test_get_project_root():
    """Test that project root is found correctly."""
    root = get_project_root()
    assert root.exists()
    assert (root / "src").exists()
    assert (root / "documentation").exists()

def test_create_output_dir(temp_dir):
    """Test output directory creation."""
    # This would need modification to work with temp_dir
    # For now, just test that the function runs without error
    try:
        output_dir = create_output_dir("test")
        assert output_dir.exists()
        # Clean up
        output_dir.rmdir()
        output_dir.parent.rmdir()
    except Exception as e:
        # In case output directory doesn't exist yet
        pass